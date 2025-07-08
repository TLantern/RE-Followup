# Cursor Closer Bot - Usage Guide

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create leads.csv**
   Create a CSV file in the root directory with headers: `name,phone,interest`
   ```csv
   name,phone,interest
   John Doe,+1234567890,Downtown Condo
   Jane Smith,+1987654321,Suburban House
   ```

3. **Set Environment Variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export TEXTBELT_API_KEY="your-textbelt-api-key"
   export TEXTBELT_WEBHOOK_URL="https://your-domain.com/sms"
   export TEXTBELT_WEBHOOK_SECRET="your-webhook-secret"
   export AGENT_TONE_SAMPLE="Hey, checking in on that property we discussed."
   export DEMO_VIDEO_URL="https://youtube.com/embed/your-video-id"
   export PORT="5000"
   export DELAY_SEC="60"
   ```

4. **Run the Bot**
   ```bash
   python main.py
   ```

5. **Access Dashboard**
   Open your browser to `http://localhost:5000` to view the leads dashboard.

## Features

- **Lead Management**: Loads leads from CSV file
- **AI Message Generation**: Uses OpenAI to generate personalized follow-ups
- **SMS Automation**: Sends messages via Textbelt
- **Reply Monitoring**: Secure webhook endpoint for incoming SMS replies
- **Dashboard**: Web interface to monitor lead status
- **Hot Lead Alerts**: Notifications when leads reply
- **Quota Monitoring**: Track Textbelt usage and remaining credits

## Configuration

### Required Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `TEXTBELT_API_KEY`: Your Textbelt API key

### Webhook Configuration (Optional but Recommended)
- `TEXTBELT_WEBHOOK_URL`: Your public webhook URL (e.g., `https://your-domain.com/sms`)
- `TEXTBELT_WEBHOOK_SECRET`: Secret key for webhook signature validation (recommended for security)

### Optional Environment Variables
- `AGENT_TONE_SAMPLE`: Example tone for AI message generation
- `DEMO_VIDEO_URL`: YouTube embed URL for dashboard
- `PORT`: Server port (default: 5000)
- `DELAY_SEC`: Delay between messages in seconds (default: 60)

## Textbelt Setup

1. **Get API Key**: Visit [textbelt.com](https://textbelt.com) to create an account and get your API key
2. **Pricing**: Textbelt offers simple pay-per-text pricing starting at $3 for 50 texts
3. **Countries Supported**: Works in US, Canada, and many international countries
4. **Quota Monitoring**: The bot automatically logs remaining quota with each message

## Webhook Setup for SMS Replies

To receive SMS replies from your leads:

1. **Deploy your application** to a publicly accessible server (e.g., Heroku, DigitalOcean, AWS)

2. **Configure webhook URL**: Set `TEXTBELT_WEBHOOK_URL` to your public endpoint:
   ```bash
   export TEXTBELT_WEBHOOK_URL="https://your-domain.com/sms"
   ```

3. **Set webhook secret** (recommended for security):
   ```bash
   export TEXTBELT_WEBHOOK_SECRET="your-random-secret-key"
   ```

4. **Test webhook**: Visit `https://your-domain.com/webhook/health` to verify it's working

### Webhook Security

The webhook endpoint includes signature validation to ensure requests are from Textbelt:
- Uses HMAC-SHA256 with your webhook secret
- Validates `X-Textbelt-Signature` header
- Automatically rejects invalid requests

### Webhook Endpoints

- `POST /sms` - Receives SMS replies from Textbelt
- `GET /webhook/health` - Health check endpoint
- `GET /` - Dashboard interface

## File Structure

```
cursor-closer-bot/
├── agents/
│   ├── __init__.py
│   ├── agent_notifier.py    # Hot lead notifications
│   ├── lead_collector.py    # CSV lead loading
│   ├── message_sender.py    # SMS via Textbelt with webhook support
│   ├── message_writer.py    # AI message generation
│   ├── reply_listener.py    # Flask webhook & dashboard with security
│   └── scheduler.py         # Follow-up automation
├── templates/
│   └── index.html          # Dashboard template
├── static/
│   └── style.css           # Dashboard styling
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── leads.csv              # Your leads data (create this)
```

## Deployment Notes

### For Production Use:
1. Use a production WSGI server (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 main:reply_app
   ```

2. Set up SSL/HTTPS for webhook security

3. Configure environment variables in your hosting platform

4. Monitor logs for webhook activity and quota usage

## Customization

- Modify `AGENT_TONE_SAMPLE` to change AI message style
- Edit `templates/index.html` to customize dashboard
- Extend `agent_notifier.py` for email/Slack notifications
- Adjust delay timing in scheduler for your use case
- Monitor quota usage via the built-in `get_quota()` function