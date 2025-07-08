"""
Test auto-responder functionality
"""
import requests
import json

# Test simulating an incoming SMS
def test_incoming_sms():
    webhook_url = "http://localhost:5000/sms"
    
    # Simulate Textbelt webhook data
    test_data = {
        "fromNumber": "+15874291448",
        "text": "Hi! I'm interested in the Downtown Condo. Can you tell me more?",
        "messageId": "test_auto_response_123"
    }
    
    print("🔔 Testing auto-responder with incoming SMS...")
    print(f"From: {test_data['fromNumber']}")
    print(f"Message: {test_data['text']}")
    print(f"Webhook URL: {webhook_url}")
    
    try:
        response = requests.post(webhook_url, json=test_data)
        print(f"\n✅ Response Status: {response.status_code}")
        print(f"📋 Response Content: {response.text}")
        
        if response.status_code == 200:
            print("\n🎉 Auto-responder test successful!")
            print("Check your phone for the automatic response!")
        else:
            print(f"\n❌ Test failed with status {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ Error testing auto-responder: {e}")

# Test health endpoint
def test_health():
    health_url = "http://localhost:5000/webhook/health"
    print(f"\n🏥 Testing health endpoint: {health_url}")
    
    try:
        response = requests.get(health_url)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_health()
    test_incoming_sms() 