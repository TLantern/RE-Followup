"""
Generate follow-ups via OpenAI.
"""
import os, logging, openai
logger = logging.getLogger(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_followup(lead, tone_sample):
    prompt = (
        f"You are a real estate agent. Example tone:\\n\"{tone_sample}\"\\n\\n"
        f"Now write a warm, concise follow-up to {lead['name']} "
        f"about their interest in {lead['interest']}. Keep it <50 words."
    )
    logger.debug("Prompt→\\n" + prompt)
    resp = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{'role':'user','content':prompt}]
    )
    text = resp.choices[0].message.content.strip()
    logger.info("Generated message: " + text)
    return text