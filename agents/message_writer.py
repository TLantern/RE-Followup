"""
Generate follow-ups via OpenAI.
"""
import os, logging
from openai import OpenAI
from .chat_storage import load_chat_history

logger = logging.getLogger(__name__)

def generate_followup(lead, tone_sample):
    # Initialize OpenAI client at runtime (after .env is loaded)
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        fallback = f"Hi {lead['name']}, just checking in about the {lead['interest']}. Let me know if you have any questions!"
        logger.info(f"Using fallback message: {fallback}")
        return fallback
    
    client = OpenAI(api_key=api_key)
    
    # Get chat history for context
    chat_history = load_chat_history(lead['phone'])
    
    # Format chat history for the prompt
    conversation_context = ""
    if chat_history:
        # Include up to the last 5 messages for context
        recent_messages = chat_history[-5:] if len(chat_history) > 5 else chat_history
        for msg in recent_messages:
            role = "Client" if msg['direction'] == 'incoming' else "Agent"
            conversation_context += f"{role}: {msg['message']}\n"
    
    # Create a more contextual prompt using the conversation history
    prompt = (
        f"You are a real estate agent named {os.getenv('AGENT_NAME', 'Alex')} helping a client. "
        f"Example tone:\n\"{tone_sample}\"\n\n"
        f"Client name: {lead['name']}\n"
        f"Client interest: {lead['interest']}\n\n"
    )
    
    # Add conversation history if available
    if conversation_context:
        prompt += f"Recent conversation:\n{conversation_context}\n"
        prompt += f"Write a helpful, natural response as the agent that addresses the client's most recent message. "
    else:
        prompt += f"Write a warm, concise follow-up to {lead['name']} about their interest in {lead['interest']}. "
    
    prompt += "Keep it conversational and under 50 words."
    
    logger.debug("Prompt→\n" + prompt)
    
    try:
        response = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=150,
            temperature=0.7
        )
        
        # Safely extract the message content
        if response and hasattr(response, 'choices') and response.choices:
            if hasattr(response.choices[0], 'message') and response.choices[0].message:
                if hasattr(response.choices[0].message, 'content'):
                    text = response.choices[0].message.content
                    if text is not None:
                        text = text.strip()
                    else:
                        text = ""
                else:
                    text = ""
            else:
                text = ""
        else:
            text = ""
            
        logger.info("Generated message: " + text)
        return text
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        # Fallback message if OpenAI fails
        fallback = f"Hi {lead['name']}, just checking in about the {lead['interest']}. Let me know if you have any questions!"
        logger.info(f"Using fallback message: {fallback}")
        return fallback