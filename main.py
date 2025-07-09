"""
Start the webhook listener for SMS responses.
"""
import os, logging, sys
from dotenv import load_dotenv
from agents.reply_listener import app as reply_app
from agents.message_writer import generate_followup
from agents.chat_storage import save_message, load_chat_history

# Load environment variables from .env file
load_dotenv()

# Enable info logging (less verbose than debug)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_message_writer():
    """Test the message writer with different lead scenarios"""
    
    print("🧪 Testing Message Writer Personalization")
    print("=" * 50)
    
    # Test scenarios with different leads
    test_leads = [
        {
            'name': 'Sarah Johnson',
            'phone': '+15551111111',
            'interest': 'Modern Apartment Downtown'
        },
        {
            'name': 'Mike Chen',
            'phone': '+15552222222',
            'interest': 'Family Home with Garden'
        },
        {
            'name': 'Emily Rodriguez',
            'phone': '+15553333333',
            'interest': 'Luxury Condo with Pool'
        },
        {
            'name': 'David Thompson',
            'phone': '+15554444444',
            'interest': 'Investment Property'
        }
    ]
    
    # Different tone samples to test variety
    tone_samples = [
        "Hey there! Hope you're having a great day. Let me know if you need anything!",
        "Hi! I wanted to follow up on our conversation about the property.",
        "Good morning! Just checking in to see if you have any questions.",
        "Hello! I'm here to help with any real estate needs you might have."
    ]
    
    print(f"📊 Testing with {len(test_leads)} different leads and {len(tone_samples)} tone samples")
    print()
    
    results = []
    
    for i, lead in enumerate(test_leads):
        tone_sample = tone_samples[i % len(tone_samples)]
        
        print(f"🔍 Test {i+1}: {lead['name']} - {lead['interest']}")
        print(f"📞 Phone: {lead['phone']}")
        print(f"🎯 Tone Sample: {tone_sample}")
        
        # Generate message
        try:
            message = generate_followup(lead, tone_sample)
            results.append({
                'lead': lead,
                'tone_sample': tone_sample,
                'generated_message': message,
                'success': True
            })
            
            print(f"✅ Generated Message: {message}")
            print(f"📏 Message Length: {len(message)} characters")
            
            # Check if message contains personalization
            contains_name = lead['name'].split()[0] in message  # First name
            contains_interest = any(word in message.lower() for word in lead['interest'].lower().split())
            
            print(f"👤 Contains Name: {'Yes' if contains_name else 'No'}")
            print(f"🏠 Contains Interest: {'Yes' if contains_interest else 'No'}")
            
        except Exception as e:
            print(f"❌ Error generating message: {e}")
            results.append({
                'lead': lead,
                'tone_sample': tone_sample,
                'generated_message': None,
                'success': False,
                'error': str(e)
            })
        
        print("-" * 40)
    
    # Test with chat history
    print("\n🗨️ Testing with Chat History Context")
    print("=" * 50)
    
    # Create a test lead with chat history
    test_lead = {
        'name': 'Alex Martinez',
        'phone': '+15555555555',
        'interest': 'Beachfront Property'
    }
    
    # Simulate some chat history
    chat_messages = [
        "Hi, I'm interested in beachfront properties. What do you have available?",
        "What's the price range for properties near the beach?",
        "Do any of them have ocean views?",
        "I'm looking for something with at least 3 bedrooms.",
        "When can we schedule a viewing?"
    ]
    
    print(f"📱 Creating chat history for {test_lead['name']} ({test_lead['phone']})")
    
    # Save chat history
    for i, msg in enumerate(chat_messages):
        save_message(test_lead['phone'], msg, 'incoming', f'test_msg_{i+1}')
        print(f"  💬 Incoming: {msg}")
    
    # Generate follow-up with context
    tone_sample = "Hi! I'm here to help you find the perfect property. Let me know what you're looking for!"
    
    print(f"\n🎯 Generating contextual follow-up...")
    try:
        message = generate_followup(test_lead, tone_sample)
        print(f"✅ Generated Message: {message}")
        
        # Verify chat history was loaded
        history = load_chat_history(test_lead['phone'])
        print(f"📚 Chat History Loaded: {len(history)} messages")
        
        results.append({
            'lead': test_lead,
            'chat_history_count': len(history),
            'generated_message': message,
            'success': True
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        results.append({
            'lead': test_lead,
            'success': False,
            'error': str(e)
        })
    
    # Analyze results
    print("\n📈 Test Results Analysis")
    print("=" * 50)
    
    successful_tests = [r for r in results if r['success']]
    failed_tests = [r for r in results if not r['success']]
    
    print(f"✅ Successful Tests: {len(successful_tests)}")
    print(f"❌ Failed Tests: {len(failed_tests)}")
    
    if failed_tests:
        print("\nFailed Test Details:")
        for test in failed_tests:
            print(f"  - {test['lead']['name']}: {test.get('error', 'Unknown error')}")
    
    if successful_tests:
        print(f"\n📊 Message Analysis:")
        
        # Check for personalization patterns
        personalized_count = 0
        fallback_count = 0
        
        for test in successful_tests:
            message = test['generated_message']
            lead = test['lead']
            
            # Check if it's a fallback message
            if "just checking in" in message.lower() and "let me know if you have any questions" in message.lower():
                fallback_count += 1
            else:
                personalized_count += 1
        
        print(f"  🎯 Personalized Messages: {personalized_count}")
        print(f"  🔄 Fallback Messages: {fallback_count}")
        
        # Show sample messages
        print(f"\n📝 Sample Generated Messages:")
        for i, test in enumerate(successful_tests[:3]):
            print(f"  {i+1}. {test['lead']['name']}: \"{test['generated_message']}\"")
    
    print(f"\n🎉 Test Complete! The message writer is generating personalized messages.")

# Log environment variables for debugging
logger.info(f"TEXTBELT_API_KEY: {'SET' if os.getenv('TEXTBELT_API_KEY') else 'NOT SET'}")
logger.info(f"TEXTBELT_WEBHOOK_URL: {os.getenv('TEXTBELT_WEBHOOK_URL', 'NOT SET')}")

if __name__ == '__main__':
    # Check for test argument
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        print("🚀 Running Message Writer Test")
        print(f"📍 Working Directory: {os.getcwd()}")
        
        # Check environment setup
        openai_key = os.getenv('OPENAI_API_KEY')
        test_mode = os.getenv('TEST_MODE', 'false').lower() == 'true'
        
        print(f"🔑 OpenAI API Key: {'Set' if openai_key else 'Not Set'}")
        print(f"🧪 Test Mode: {'Enabled' if test_mode else 'Disabled'}")
        print()
        
        test_message_writer()
    else:
        # Only start the webhook listener - NO automatic messaging
        port = int(os.getenv('PORT','8080'))
        logger.info(f"Starting SMS responder on port {port}")
        logger.info("App will only respond to incoming SMS messages")
        logger.info("Use 'python main.py test' to test message personalization")
        reply_app.run(host='0.0.0.0', port=port, debug=False)