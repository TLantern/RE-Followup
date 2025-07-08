"""
Send SMS via Twilio.
"""
import os, logging
from twilio.rest import Client
logger = logging.getLogger(__name__)
client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
FROM = os.getenv('TWILIO_PHONE_NUMBER')

def send_sms(to, body):
    try:
        msg = client.messages.create(body=body, from_=FROM, to=to)
        logger.info(f"SMS→{to}, SID:{msg.sid}")
        return msg.sid
    except Exception as e:
        logger.error("SMS error: " + str(e))
        return None