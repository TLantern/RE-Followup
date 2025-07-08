"""
Send a wave of follow-ups.
"""
import time, logging
from .lead_collector import load_leads_from_csv
from .message_writer import generate_followup
from .message_sender import send_sms

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_wave(tone_sample, delay=60):
    leads = load_leads_from_csv()
    for lead in leads:
        logger.info("Processing lead: " + str(lead))
        msg = generate_followup(lead, tone_sample)
        send_sms(lead['phone'], msg)
        time.sleep(delay)