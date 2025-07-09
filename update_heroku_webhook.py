#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update the webhook URL with the Heroku app URL.
"""
import os
import requests
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def update_webhook_url(heroku_app_name):
    """Update the webhook URL in the .env file with Heroku app URL"""
    try:
        # Construct the Heroku app URL
        heroku_url = f"https://{heroku_app_name}.herokuapp.com"
        
        # Get the current directory
        current_dir = Path(__file__).parent.absolute()
        
        # Path to .env file
        env_file = current_dir / ".env"
        
        if not env_file.exists():
            print("❌ .env file not found")
            # Create a new .env file
            with open(env_file, 'w') as f:
                f.write(f"TEXTBELT_WEBHOOK_URL={heroku_url}/sms\n")
            print("✅ Created new .env file with webhook URL")
            return True
        
        # Read the .env file
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Update the webhook URL
        webhook_updated = False
        with open(env_file, 'w') as f:
            for line in lines:
                if line.startswith("TEXTBELT_WEBHOOK_URL="):
                    f.write(f"TEXTBELT_WEBHOOK_URL={heroku_url}/sms\n")
                    webhook_updated = True
                else:
                    f.write(line)
            
            # Add the webhook URL if it doesn't exist
            if not webhook_updated:
                f.write(f"\nTEXTBELT_WEBHOOK_URL={heroku_url}/sms\n")
        
        print(f"✅ Webhook URL updated to {heroku_url}/sms")
        return True
    
    except Exception as e:
        print(f"❌ Error updating webhook URL: {e}")
        return False

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("❌ Please provide your Heroku app name")
        print("Usage: python update_heroku_webhook.py your-app-name")
        return False
    
    heroku_app_name = sys.argv[1]
    print(f"🔄 Updating webhook URL with Heroku app: {heroku_app_name}")
    
    # Update the webhook URL
    if update_webhook_url(heroku_app_name):
        print("✅ Webhook URL updated successfully")
        
        # Test the webhook URL
        heroku_url = f"https://{heroku_app_name}.herokuapp.com"
        print(f"🔍 Testing webhook health at {heroku_url}/webhook/health")
        
        try:
            response = requests.get(f"{heroku_url}/webhook/health", timeout=10)
            if response.status_code == 200:
                print("✅ Webhook health check successful")
                print(f"Response: {response.json()}")
            else:
                print(f"⚠️ Webhook health check returned status code {response.status_code}")
        except Exception as e:
            print(f"⚠️ Could not reach webhook health endpoint: {e}")
            print("Make sure your Heroku app is deployed and running")
        
        return True
    else:
        print("❌ Failed to update webhook URL")
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1) 