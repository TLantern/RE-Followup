#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Update the webhook URL with the ngrok URL.
"""
import os
import json
import requests
import subprocess
import time
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_ngrok_url():
    """Get the ngrok public URL"""
    try:
        # Try to get the URL from the ngrok API
        response = requests.get("http://localhost:4040/api/tunnels")
        data = response.json()
        
        if "tunnels" in data and len(data["tunnels"]) > 0:
            for tunnel in data["tunnels"]:
                if tunnel["proto"] == "https":
                    return tunnel["public_url"]
            
            # If no HTTPS tunnel found, use the first one
            return data["tunnels"][0]["public_url"]
        else:
            print("❌ No active ngrok tunnels found")
            return None
    
    except Exception as e:
        print(f"❌ Error getting ngrok URL: {e}")
        return None

def update_webhook_url(ngrok_url):
    """Update the webhook URL in the .env file"""
    try:
        # Get the current directory
        current_dir = Path(__file__).parent.absolute()
        
        # Path to .env file
        env_file = current_dir / ".env"
        
        if not env_file.exists():
            print("❌ .env file not found")
            return False
        
        # Read the .env file
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Update the webhook URL
        webhook_updated = False
        with open(env_file, 'w') as f:
            for line in lines:
                if line.startswith("TEXTBELT_WEBHOOK_URL="):
                    f.write(f"TEXTBELT_WEBHOOK_URL={ngrok_url}/sms\n")
                    webhook_updated = True
                else:
                    f.write(line)
            
            # Add the webhook URL if it doesn't exist
            if not webhook_updated:
                f.write(f"\nTEXTBELT_WEBHOOK_URL={ngrok_url}/sms\n")
        
        print(f"✅ Webhook URL updated to {ngrok_url}/sms")
        return True
    
    except Exception as e:
        print(f"❌ Error updating webhook URL: {e}")
        return False

def main():
    """Main function"""
    print("🔍 Looking for ngrok URL...")
    
    # Try to get the ngrok URL
    ngrok_url = get_ngrok_url()
    
    if not ngrok_url:
        print("❌ Failed to get ngrok URL. Make sure ngrok is running.")
        return False
    
    print(f"✅ Found ngrok URL: {ngrok_url}")
    
    # Update the webhook URL
    if update_webhook_url(ngrok_url):
        print("✅ Webhook URL updated successfully")
        print("🔄 Restarting the service to apply changes...")
        
        # Stop the current service
        subprocess.run([sys.executable, "stop_background.py"])
        
        # Start the service again
        subprocess.run([sys.executable, "run_background.py"])
        
        print("✅ Service restarted successfully")
        return True
    else:
        print("❌ Failed to update webhook URL")
        return False

if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1) 