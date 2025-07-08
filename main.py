"""
Start the scheduler and dashboard listener.
"""
import threading, os, logging
from dotenv import load_dotenv
from agents.scheduler import send_wave
from agents.reply_listener import app as reply_app

# Load environment variables from .env file
load_dotenv()

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def start_wave():
    tone = os.getenv('AGENT_TONE_SAMPLE', "Hey, checking in on that property we discussed.")
    send_wave(tone, delay=int(os.getenv('DELAY_SEC','60')))

if __name__ == '__main__':
    # Log environment variables for debugging
    logger.info(f"TEXTBELT_API_KEY: {'SET' if os.getenv('TEXTBELT_API_KEY') else 'NOT SET'}")
    logger.info(f"TEXTBELT_WEBHOOK_URL: {os.getenv('TEXTBELT_WEBHOOK_URL', 'NOT SET')}")
    
    threading.Thread(target=start_wave, daemon=True).start()
    port = int(os.getenv('PORT','5000'))
    logger.info(f"Starting app on port {port}")
    reply_app.run(host='0.0.0.0', port=port, debug=True)