"""
Test the background SMS auto-responder service.
"""
import requests
import json

def test_background_service():
    """Test if the background service is responding correctly"""
    
    print("🧪 Testing Background SMS Auto-Responder Service")
    print("=" * 50)
    
    # Test health endpoint
    try:
        print("📡 Testing health endpoint...")
        response = requests.get('http://localhost:5000/webhook/health')
        print(f"✅ Health Status: {response.status_code}")
        print(f"📋 Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test SMS webhook endpoint
    try:
        print("\n📱 Testing SMS webhook endpoint...")
        test_data = {
            "fromNumber": "+15874291448",
            "text": "Testing background service - please respond!",
            "messageId": "bg_service_test_123"
        }
        
        response = requests.post(
            'http://localhost:5000/sms',
            headers={'Content-Type': 'application/json'},
            json=test_data
        )
        
        print(f"✅ SMS Webhook Status: {response.status_code}")
        print(f"📋 Response: {response.json()}")
        
        if response.status_code == 200:
            print("\n🎉 Background service is working correctly!")
            print("📱 Check your phone for the auto-response message")
            return True
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ SMS webhook test failed: {e}")
        return False

def check_service_status():
    """Check if the background service is running"""
    
    try:
        response = requests.get('http://localhost:5000/webhook/health', timeout=5)
        if response.status_code == 200:
            print("✅ Background service is running")
            return True
        else:
            print(f"⚠️ Service responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Background service is not running")
        return False
    except Exception as e:
        print(f"❌ Error checking service: {e}")
        return False

if __name__ == "__main__":
    if check_service_status():
        test_background_service()
    else:
        print("\n💡 To start the background service, run: python run_background.py") 