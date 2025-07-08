"""
Simple chat storage system for tracking SMS conversations
"""
import json
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

CHAT_STORAGE_DIR = "chat_history"

def ensure_storage_dir():
    """Ensure the chat storage directory exists"""
    if not os.path.exists(CHAT_STORAGE_DIR):
        os.makedirs(CHAT_STORAGE_DIR)

def get_chat_file(phone_number):
    """Get the chat file path for a phone number"""
    # Clean phone number for filename (remove + and other chars)
    clean_phone = phone_number.replace('+', '').replace('-', '').replace(' ', '')
    return os.path.join(CHAT_STORAGE_DIR, f"chat_{clean_phone}.json")

def load_chat_history(phone_number):
    """Load chat history for a phone number"""
    try:
        chat_file = get_chat_file(phone_number)
        if os.path.exists(chat_file):
            with open(chat_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        logger.error(f"Error loading chat history for {phone_number}: {e}")
        return []

def save_message(phone_number, message, direction, message_id=None):
    """
    Save a message to chat history
    direction: 'outgoing' or 'incoming'
    """
    try:
        ensure_storage_dir()
        
        # Load existing history
        history = load_chat_history(phone_number)
        
        # Create new message entry
        message_entry = {
            'timestamp': datetime.now().isoformat(),
            'direction': direction,
            'message': message,
            'message_id': message_id
        }
        
        # Add to history
        history.append(message_entry)
        
        # Save back to file
        chat_file = get_chat_file(phone_number)
        with open(chat_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {direction} message for {phone_number}")
        
    except Exception as e:
        logger.error(f"Error saving message for {phone_number}: {e}")

def get_all_phone_numbers():
    """Get all phone numbers that have chat history"""
    try:
        ensure_storage_dir()
        phone_numbers = []
        
        for filename in os.listdir(CHAT_STORAGE_DIR):
            if filename.startswith('chat_') and filename.endswith('.json'):
                # Extract phone number from filename
                clean_phone = filename[5:-5]  # Remove 'chat_' and '.json'
                # Add + back for US numbers
                if len(clean_phone) == 11 and clean_phone.startswith('1'):
                    phone_numbers.append(f"+{clean_phone}")
                elif len(clean_phone) == 10:
                    phone_numbers.append(f"+1{clean_phone}")
                else:
                    phone_numbers.append(f"+{clean_phone}")
        
        return phone_numbers
    except Exception as e:
        logger.error(f"Error getting phone numbers: {e}")
        return [] 