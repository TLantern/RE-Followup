"""
Flask webhook for incoming SMS and serve dashboard.
"""
import os, logging, hmac, hashlib
from flask import Flask, request, render_template, abort
from .agent_notifier import notify_agent
from .lead_collector import load_leads_from_csv

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
            logger.error("No signature provided in webhook")
            return False
        
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
        return True  # Allow through if validation fails

@app.route('/sms', methods=['POST'])
def sms_reply():
    """Handle incoming SMS replies from Textbelt webhook"""
    try:
        logger.info("SMS webhook called")
        
        # Get raw payload for signature validation
        payload = request.get_data()
        signature = request.headers.get('X-Textbelt-Signature')
        
        logger.debug(f"Payload length: {len(payload)}")
        logger.debug(f"Signature: {signature}")
        
        # Validate webhook signature for security
        if not validate_textbelt_webhook(payload, signature):
            logger.error("Invalid webhook signature")
            abort(401)
        
        logger.info("Signature validation passed")
        
        # Parse Textbelt webhook data
        if request.is_json:
            data = request.get_json()
            logger.debug(f"JSON data: {data}")
            
            # Textbelt webhook format
            from_number = data.get('fromNumber')
            message_text = data.get('text')
            message_id = data.get('messageId')
            
            logger.info(f"Textbelt webhook - MessageID: {message_id}, From: {from_number}")
            
        else:
            logger.info("Processing form data")
            # Fallback to form data for backward compatibility
            from_number = request.form.get('fromNumber', request.form.get('From', request.form.get('from')))
            message_text = request.form.get('text', request.form.get('Body'))
            message_id = request.form.get('messageId')
            logger.debug(f"Form data - From: {from_number}, Text: {message_text}")
        
        if from_number and message_text:
            logger.info(f"SMS Reply from {from_number}: {message_text}")
            notify_agent(from_number, message_text)
            
            # Return success response as expected by Textbelt
            return {'success': True}, 200
        else:
            logger.warning(f"Incomplete webhook data - from: {from_number}, text: {message_text}")
            return {'error': 'Missing required fields'}, 400
        
    except Exception as e:
        logger.error(f"Error processing Textbelt webhook: {e}", exc_info=True)
        return {'error': 'Internal server error'}, 500

@app.route('/webhook/health', methods=['GET'])
def webhook_health():
    """Health check endpoint for webhook"""
    return {'status': 'healthy', 'service': 'textbelt-webhook'}, 200

@app.route('/')
def dashboard():
    leads = load_leads_from_csv()
    for lead in leads: lead['status'] = 'Sent'
    demo = os.getenv('DEMO_VIDEO_URL', '')
    return render_template('index.html', leads=leads, demo_video=demo)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT',5000)))