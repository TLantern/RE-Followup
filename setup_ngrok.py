#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup ngrok with your authtoken and start a tunnel to your local server.
"""
import os
import subprocess
import sys
import time
from pathlib import Path

def setup_ngrok():
    """Setup ngrok with your authtoken and start a tunnel"""
    
    # Check if ngrok is available
    current_dir = Path(__file__).parent.absolute()
    ngrok_path = current_dir / "ngrok"
    
    if not ngrok_path.exists():
        print("❌ ngrok not found. Please download it from https://ngrok.com/download")
        return False
    
    # Check if ngrok is already authenticated
    try:
        result = subprocess.run([str(ngrok_path), 'config', 'check'], 
                               capture_output=True, text=True)
        if "authtoken is not set" not in result.stdout and "authtoken is not set" not in result.stderr:
            print("✅ ngrok is already authenticated")
        else:
            # Ask for authtoken
            print("🔑 ngrok requires authentication with an authtoken.")
            print("1. Sign up for a free account at https://dashboard.ngrok.com/signup")
            print("2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken")
            authtoken = input("Enter your ngrok authtoken: ").strip()
            
            if not authtoken:
                print("❌ No authtoken provided. Cannot continue.")
                return False
            
            # Set the authtoken
            subprocess.run([str(ngrok_path), 'config', 'add-authtoken', authtoken])
            print("✅ ngrok authtoken configured successfully")
    
    except Exception as e:
        print(f"❌ Error configuring ngrok: {e}")
        return False
    
    # Start the ngrok tunnel
    port = 8080  # Use the same port as in main.py
    print(f"🚀 Starting ngrok tunnel to port {port}...")
    
    # Start ngrok in a new process
    try:
        # On Windows, use CREATE_NEW_CONSOLE
        if os.name == 'nt':
            subprocess.Popen([str(ngrok_path), 'http', str(port)], 
                            creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            # On Unix-like systems, start in background
            subprocess.Popen([str(ngrok_path), 'http', str(port)], 
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ ngrok tunnel started")
        print("🌐 To see your public URL, run: ./ngrok status")
        print("📊 Web interface available at: http://localhost:4040")
        
        return True
    
    except Exception as e:
        print(f"❌ Failed to start ngrok tunnel: {e}")
        return False

if __name__ == "__main__":
    setup_ngrok() 