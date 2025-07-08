#!/usr/bin/env python3
"""
Update Textbelt webhook URL to use ngrok tunnel
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def update_webhook_url(new_ngrok_url):
    """
    Update the webhook URL by sending a test message with the new webhook
    """
    api_key = os.getenv('TEXTBELT_API_KEY')
    
    if not api_key:
        print("❌ TEXTBELT_API_KEY not found in environment variables")
        return False
    
    # Add /sms to the ngrok URL if not present
    if not new_ngrok_url.endswith('/sms'):
        webhook_url = f"{new_ngrok_url}/sms"
    else:
        webhook_url = new_ngrok_url
    
    print(f"🔄 Updating Textbelt webhook to: {webhook_url}")
    
    # Test the webhook URL first
    try:
        test_response = requests.get(webhook_url.replace('/sms', '/webhook/health'))
        if test_response.status_code != 200:
            print(f"⚠️ Warning: Webhook health check failed ({test_response.status_code})")
        else:
            print("✅ Webhook health check passed")
    except Exception as e:
        print(f"⚠️ Warning: Could not test webhook: {e}")
    
    # Send a test message to yourself to register the new webhook
    test_phone = "+15874291448"  # Your phone number
    test_message = "🔧 Webhook updated! Your SMS auto-responder is now connected to your local service."
    
    payload = {
        'phone': test_phone,
        'message': test_message,
        'key': api_key,
        'replyWebhookUrl': webhook_url
    }
    
    try:
        response = requests.post('https://textbelt.com/text', data=payload)
        result = response.json()
        
        if result.get('success'):
            print(f"✅ Webhook updated successfully!")
            print(f"📱 Test message sent to {test_phone}")
            print(f"🔗 New webhook URL: {webhook_url}")
            
            # Update .env file
            update_env_file(webhook_url)
            return True
        else:
            print(f"❌ Failed to update webhook: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating webhook: {e}")
        return False

def update_env_file(webhook_url):
    """Update the .env file with the new webhook URL"""
    try:
        # Read existing .env file
        env_content = []
        env_file = '.env'
        
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                env_content = f.readlines()
        
        # Update or add TEXTBELT_WEBHOOK_URL
        webhook_line = f"TEXTBELT_WEBHOOK_URL={webhook_url}\n"
        webhook_updated = False
        
        for i, line in enumerate(env_content):
            if line.startswith('TEXTBELT_WEBHOOK_URL='):
                env_content[i] = webhook_line
                webhook_updated = True
                break
        
        if not webhook_updated:
            env_content.append(webhook_line)
        
        # Write back to .env file
        with open(env_file, 'w') as f:
            f.writelines(env_content)
        
        print(f"📝 Updated .env file with new webhook URL")
        
    except Exception as e:
        print(f"⚠️ Could not update .env file: {e}")

if __name__ == "__main__":
    ngrok_url = input("🔗 Enter your ngrok URL (e.g., https://abcd-1234.ngrok.io): ").strip()
    
    if not ngrok_url:
        print("❌ No URL provided")
        exit(1)
    
    if not ngrok_url.startswith('https://'):
        print("❌ URL must start with https://")
        exit(1)
    
    update_webhook_url(ngrok_url) 