"""
Generate follow-ups via OpenAI.
"""
import os, logging
from openai import OpenAI

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
    
    prompt = (
        f"You are a real estate agent. Example tone:\n\"{tone_sample}\"\n\n"
        f"Now write a warm, concise follow-up to {lead['name']} "
        f"about their interest in {lead['interest']}. Keep it <50 words."
    )
    logger.debug("Prompt→\n" + prompt)
    
    try:
        response = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=100,
            temperature=0.7
        )
        text = response.choices[0].message.content.strip()
        logger.info("Generated message: " + text)
        return text
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        # Fallback message if OpenAI fails
        fallback = f"Hi {lead['name']}, just checking in about the {lead['interest']}. Let me know if you have any questions!"
        logger.info(f"Using fallback message: {fallback}")
        return fallback