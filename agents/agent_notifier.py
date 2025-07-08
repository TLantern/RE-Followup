"""
Notify agent on hot lead.
"""
import logging
logger = logging.getLogger(__name__)

def notify_agent(from_number, message):
    logger.info(f"[🔥 HOT LEAD] {from_number} replied: {message}")
    # extend: email/Slack/Telegram here