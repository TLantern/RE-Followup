"""
Test SMS sending with webhook
"""
import os, logging
from dotenv import load_dotenv
from agents.message_sender import send_sms

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()

# Test sending SMS to yourself
test_phone = "+15874291448"  # Your phone number
test_message = "This is a test message from your RE-Followup bot. Reply to test the webhook!"

print(f"TEXTBELT_API_KEY: {'SET' if os.getenv('TEXTBELT_API_KEY') else 'NOT SET'}")
print(f"API Key value: {os.getenv('TEXTBELT_API_KEY')[:10]}..." if os.getenv('TEXTBELT_API_KEY') else "None")
print(f"TEXTBELT_WEBHOOK_URL: {os.getenv('TEXTBELT_WEBHOOK_URL', 'NOT SET')}")
print(f"Sending test SMS to {test_phone}...")

result = send_sms(test_phone, test_message)

if result:
    print(f"✅ SMS sent successfully! Message ID: {result}")
    print("📱 Check your phone and reply to test the webhook")
else:
    print("❌ SMS failed to send") 