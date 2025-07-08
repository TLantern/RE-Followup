"""
Simple webhook test
"""
import requests

# Test without signature (should work as no secret is set)
webhook_url = "http://localhost:5000/sms"
test_data = {
    "fromNumber": "+15874291448",
    "text": "Test message",
    "messageId": "test123"
}

print("Testing webhook without signature...")
response = requests.post(webhook_url, json=test_data)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")

# Also test with form data (fallback format)
print("\nTesting with form data...")
form_data = {
    "fromNumber": "+15874291448",
    "text": "Test form message"
}
response2 = requests.post(webhook_url, data=form_data)
print(f"Status: {response2.status_code}")
print(f"Response: {response2.text}") 