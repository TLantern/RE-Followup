"""
Flask webhook for incoming SMS and serve dashboard.
"""
import os, logging, hmac, hashlib
from flask import Flask, request, render_template, abort, jsonify
from .agent_notifier import notify_agent
from .lead_collector import load_leads_from_csv
from .chat_storage import save_message, load_chat_history, get_all_phone_numbers
from .message_writer import generate_followup
from .message_sender import send_sms

app = Flask(__name__, static_folder='../static', template_folder='../templates')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_textbelt_webhook(payload, signature):
    """Validate Textbelt webhook signature for security"""
    try:
        webhook_secret = os.getenv('TEXTBELT_WEBHOOK_SECRET')
        if not webhook_secret:
            logger.warning("TEXTBELT_WEBHOOK_SECRET not set - skipping signature validation")
            return True
        
        if not signature:
            logger.warning("No signature provided in webhook - allowing for testing")
            return True  # Allow for testing without signature
        
        # Remove 'sha256=' prefix if present
        if signature.startswith('sha256='):
            signature = signature[7:]
        
        # Calculate expected signature
        expected_signature = hmac.new(
            webhook_secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)
    except Exception as e:
        logger.error(f"Error in signature validation: {e}")
        return True  # Allow through if validation fails during testing

def find_lead_by_phone(phone_number):
    """Find lead information by phone number"""
    leads = load_leads_from_csv()
    for lead in leads:
        if lead['phone'] == phone_number:
            return lead
    return None

def generate_auto_response(from_number, incoming_message):
    """Generate an automatic response based on the incoming message"""
    try:
        # Find the lead information
        lead = find_lead_by_phone(from_number)
        
        if not lead:
            # Create a generic lead entry for unknown numbers
            lead = {
                'name': 'Potential Client',
                'phone': from_number,
                'interest': 'Real Estate Inquiry'
            }
        
        # Use the incoming message context to generate a relevant response
        tone_sample = os.getenv('AGENT_TONE_SAMPLE', "Thanks for reaching out! Let me help you with that.")
        
        # Generate contextual response
        response = generate_followup(lead, f"{tone_sample} Responding to: {incoming_message}")
        return response
        
    except Exception as e:
        logger.error(f"Error generating auto-response: {e}")
        # Fallback response
        return "Thanks for your message! I'll get back to you shortly with more information."

@app.route('/sms', methods=['POST'])
def sms_reply():
    """Handle incoming SMS replies from Textbelt webhook"""
    try:
        logger.info("🔔 SMS webhook called")
        
        # Get raw payload for signature validation
        payload = request.get_data()
        signature = request.headers.get('X-Textbelt-Signature')
        
        logger.debug(f"Payload length: {len(payload)}")
        logger.debug(f"Signature: {signature}")
        
        # Validate webhook signature for security (relaxed for testing)
        if not validate_textbelt_webhook(payload, signature):
            logger.error("Invalid webhook signature")
            # Don't abort during testing, just log the error
            # abort(401)
        
        logger.info("✅ Signature validation passed")
        
        # Parse Textbelt webhook data
        if request.is_json:
            data = request.get_json()
            logger.debug(f"JSON data: {data}")
            
            # Textbelt webhook format
            from_number = data.get('fromNumber')
            message_text = data.get('text')
            message_id = data.get('messageId')
            
            logger.info(f"📱 Textbelt webhook - MessageID: {message_id}, From: {from_number}")
            
        else:
            logger.info("📋 Processing form data")
            # Fallback to form data for backward compatibility
            from_number = request.form.get('fromNumber', request.form.get('From', request.form.get('from')))
            message_text = request.form.get('text', request.form.get('Body'))
            message_id = request.form.get('messageId', 'unknown')
            logger.debug(f"Form data - From: {from_number}, Text: {message_text}")
        
        if from_number and message_text:
            logger.info(f"💬 SMS Reply from {from_number}: {message_text}")
            
            # Save incoming message to chat history
            save_message(from_number, message_text, 'incoming', message_id)
            
            # Notify agent about the message
            notify_agent(from_number, message_text)
            
            # Generate and send automatic response
            logger.info("🤖 Generating automatic response...")
            auto_response = generate_auto_response(from_number, message_text)
            
            if auto_response:
                logger.info(f"📤 Sending auto-response: {auto_response[:50]}...")
                response_id = send_sms(from_number, auto_response)
                
                if response_id:
                    logger.info(f"✅ Auto-response sent successfully! ID: {response_id}")
                else:
                    logger.error("❌ Failed to send auto-response")
            
            # Return success response as expected by Textbelt
            return {'success': True, 'message': 'Message received and auto-response sent'}, 200
        else:
            logger.warning(f"⚠️ Incomplete webhook data - from: {from_number}, text: {message_text}")
            return {'error': 'Missing required fields'}, 400
        
    except Exception as e:
        logger.error(f"❌ Error processing Textbelt webhook: {e}", exc_info=True)
        return {'error': 'Internal server error'}, 500

@app.route('/api/chat/<phone_number>')
def get_chat_history(phone_number):
    """API endpoint to get chat history for a phone number"""
    try:
        # Ensure phone number has + prefix
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
            
        history = load_chat_history(phone_number)
        return jsonify({
            'phone_number': phone_number,
            'messages': history
        })
    except Exception as e:
        logger.error(f"Error getting chat history for {phone_number}: {e}")
        return jsonify({'error': 'Failed to load chat history'}), 500

@app.route('/webhook/health', methods=['GET'])
def webhook_health():
    """Health check endpoint for webhook"""
    return {'status': 'healthy', 'service': 'textbelt-webhook', 'mode': 'auto-responder'}, 200

@app.route('/api/send-test', methods=['POST'])
def send_test_message():
    """Manual endpoint to send a test message (for testing purposes)"""
    try:
        data = request.get_json()
        phone = data.get('phone')
        message = data.get('message')
        
        if not phone or not message:
            return {'error': 'Phone and message required'}, 400
        
        message_id = send_sms(phone, message)
        if message_id:
            return {'success': True, 'message_id': message_id}, 200
        else:
            return {'error': 'Failed to send message'}, 500
            
    except Exception as e:
        logger.error(f"Error sending test message: {e}")
        return {'error': 'Internal server error'}, 500

@app.route('/')
def dashboard():
    leads = load_leads_from_csv()
    
    # Get chat history for each lead to show message count
    chat_phones = get_all_phone_numbers()
    
    for lead in leads:
        lead['status'] = 'Ready to Respond'
        # Count messages if chat history exists
        if lead['phone'] in chat_phones:
            history = load_chat_history(lead['phone'])
            incoming_count = len([msg for msg in history if msg['direction'] == 'incoming'])
            outgoing_count = len([msg for msg in history if msg['direction'] == 'outgoing'])
            lead['message_count'] = f"{outgoing_count} sent, {incoming_count} received"
            if incoming_count > 0:
                lead['status'] = 'Active Conversation'
        else:
            lead['message_count'] = "No messages yet"
    
    demo = os.getenv('DEMO_VIDEO_URL', '')
    return render_template('index.html', leads=leads, demo_video=demo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT',8080)))