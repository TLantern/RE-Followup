"""
Send SMS via Textbelt.
"""
import os, logging, requests
from .chat_storage import save_message

logger = logging.getLogger(__name__)

TEXTBELT_API_URL = "https://textbelt.com/text"

def send_sms(to, body):
    try:
        # Get API key and webhook URL at runtime (after .env is loaded)
        api_key = os.getenv('TEXTBELT_API_KEY')
        webhook_url = os.getenv('TEXTBELT_WEBHOOK_URL')
        test_mode = os.getenv('TEST_MODE', 'false').lower() == 'true'
        
        if not api_key and not test_mode:
            logger.error("TEXTBELT_API_KEY not found in environment variables")
            return None
        
        logger.debug(f"Using API key: {'SET' if api_key else 'NOT SET'}")
        
        # Test mode - don't actually send SMS
        if test_mode:
            logger.info(f"TEST MODE: Would send to {to}: {body}")
            test_message_id = f"test_{hash(body) % 10000}"
            
            # Save outgoing message to chat history
            save_message(to, body, 'outgoing', test_message_id)
            
            return test_message_id
        
        # Prepare the payload for Textbelt API
        payload = {
            'phone': to,
            'message': body,
            'key': api_key
        }
        
        # Add webhook URL if configured for reply handling
        if webhook_url:
            payload['replyWebhookUrl'] = webhook_url
            logger.debug(f"Including webhook URL: {webhook_url}")
        
        logger.debug(f"Sending to Textbelt with payload: {payload}")
        
        # Send SMS via Textbelt API
        response = requests.post(TEXTBELT_API_URL, data=payload)
        response_data = response.json()
        
        logger.debug(f"Textbelt response: {response_data}")
        
        if response_data.get('success'):
            message_id = response_data.get('textId', 'unknown')
            quota_remaining = response_data.get('quotaRemaining', 'unknown')
            logger.info(f"SMS→{to}, TextID:{message_id}, Quota:{quota_remaining}")
            
            # Save outgoing message to chat history
            save_message(to, body, 'outgoing', message_id)
            
            return message_id
        else:
            error_message = response_data.get('error', 'Unknown error')
            logger.error(f"SMS error: {error_message}")
            return None
            
    except Exception as e:
        logger.error("SMS error: " + str(e))
        return None

def get_quota():
    """Check remaining Textbelt quota"""
    try:
        api_key = os.getenv('TEXTBELT_API_KEY')
        if not api_key:
            logger.error("TEXTBELT_API_KEY not found in environment variables")
            return None
            
        payload = {'key': api_key}
        response = requests.post('https://textbelt.com/quota', data=payload)
        data = response.json()
        
        if data.get('success'):
            return data.get('quotaRemaining', 0)
        else:
            logger.error(f"Quota check error: {data.get('error')}")
            return None
    except Exception as e:
        logger.error(f"Quota check error: {e}")
        return None