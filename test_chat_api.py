"""
Test chat history API
"""
import requests

# Test the chat API
phone = "15874291448"
url = f"http://localhost:5000/api/chat/{phone}"

print(f"Testing chat API: {url}")

try:
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")

# Also test health endpoint
print(f"\nTesting health endpoint...")
try:
    response = requests.get("http://localhost:5000/webhook/health")
    print(f"Health status: {response.status_code}")
    print(f"Health response: {response.text}")
except Exception as e:
    print(f"Error: {e}") 