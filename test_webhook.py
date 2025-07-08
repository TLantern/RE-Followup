"""
Test webhook endpoint
"""
import requests
import json

# Test webhook with mock SMS reply
webhook_url = "http://localhost:5000/sms"
test_data = {
    "fromNumber": "+15874291448",
    "text": "I am very interested!",
    "messageId": "test123"
}

print(f"Testing webhook: {webhook_url}")
print(f"Sending data: {json.dumps(test_data, indent=2)}")

try:
    response = requests.post(webhook_url, json=test_data)
    print(f"Response status: {response.status_code}")
    print(f"Response content: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Also test health endpoint
health_url = "http://localhost:5000/webhook/health"
print(f"\nTesting health endpoint: {health_url}")
try:
    response = requests.get(health_url)
    print(f"Health status: {response.status_code}")
    print(f"Health response: {response.text}")
except Exception as e:
    print(f"Error: {e}") 