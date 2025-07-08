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
   export TWILIO_ACCOUNT_SID="your-twilio-account-sid"
   export TWILIO_AUTH_TOKEN="your-twilio-auth-token"
   export TWILIO_PHONE_NUMBER="your-twilio-phone-number"
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
- **SMS Automation**: Sends messages via Twilio
- **Reply Monitoring**: Webhook endpoint for incoming SMS replies
- **Dashboard**: Web interface to monitor lead status
- **Hot Lead Alerts**: Notifications when leads reply

## Configuration

### Required Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `TWILIO_ACCOUNT_SID`: Twilio account SID
- `TWILIO_AUTH_TOKEN`: Twilio auth token
- `TWILIO_PHONE_NUMBER`: Your Twilio phone number

### Optional Environment Variables
- `AGENT_TONE_SAMPLE`: Example tone for AI message generation
- `DEMO_VIDEO_URL`: YouTube embed URL for dashboard
- `PORT`: Server port (default: 5000)
- `DELAY_SEC`: Delay between messages in seconds (default: 60)

## Webhook Setup

For SMS replies, configure your Twilio webhook URL to point to:
```
https://your-domain.com/sms
```

## File Structure

```
cursor-closer-bot/
├── agents/
│   ├── __init__.py
│   ├── agent_notifier.py    # Hot lead notifications
│   ├── lead_collector.py    # CSV lead loading
│   ├── message_sender.py    # SMS via Twilio
│   ├── message_writer.py    # AI message generation
│   ├── reply_listener.py    # Flask webhook & dashboard
│   └── scheduler.py         # Follow-up automation
├── templates/
│   └── index.html          # Dashboard template
├── static/
│   └── style.css           # Dashboard styling
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── leads.csv              # Your leads data (create this)
```

## Customization

- Modify `AGENT_TONE_SAMPLE` to change AI message style
- Edit `templates/index.html` to customize dashboard
- Extend `agent_notifier.py` for email/Slack notifications
- Adjust delay timing in scheduler for your use case