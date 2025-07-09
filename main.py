"""
Start the webhook listener for SMS responses.
"""
import os, logging
from dotenv import load_dotenv
from agents.reply_listener import app as reply_app

# Load environment variables from .env file
load_dotenv()

# Enable info logging (less verbose than debug)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Log environment variables for debugging
logger.info(f"TEXTBELT_API_KEY: {'SET' if os.getenv('TEXTBELT_API_KEY') else 'NOT SET'}")
logger.info(f"TEXTBELT_WEBHOOK_URL: {os.getenv('TEXTBELT_WEBHOOK_URL', 'NOT SET')}")

if __name__ == '__main__':
    # Only start the webhook listener - NO automatic messaging
    port = int(os.getenv('PORT','8080'))
    logger.info(f"Starting SMS responder on port {port}")
    logger.info("App will only respond to incoming SMS messages")
    reply_app.run(host='0.0.0.0', port=port, debug=False)