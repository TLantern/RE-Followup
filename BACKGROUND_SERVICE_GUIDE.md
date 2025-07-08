# SMS Auto-Responder Background Service Guide

## Overview

Your SMS auto-responder can now run in the background continuously, allowing it to respond to incoming text messages even when you're not actively monitoring the application.

## Quick Start

### 1. Start the Background Service

**Option A: Using Python script**
```bash
python run_background.py
```

**Option B: Using Windows batch file**
```bash
start_service.bat
```

### 2. Check Service Status
```bash
python stop_background.py status
```

### 3. Stop the Service
```bash
python stop_background.py
```
or
```bash
stop_service.bat
```

## Features

✅ **Background Operation**: Runs independently without keeping a terminal open  
✅ **Automatic Logging**: All activity logged to `logs/auto_responder.log`  
✅ **Error Tracking**: Errors logged to `logs/auto_responder_error.log`  
✅ **Health Monitoring**: Built-in health check endpoint  
✅ **Windows Startup**: Optional auto-start on system boot  

## Advanced Setup

### Auto-Start on Windows Boot

To have the SMS auto-responder start automatically when you log into Windows:

```bash
python install_startup.py
```

To remove auto-start:
```bash
python uninstall_startup.py
```

### Monitor Service Logs

View real-time logs:
```bash
# On Windows with PowerShell
Get-Content logs\auto_responder.log -Wait

# Or use any text editor to view:
# logs/auto_responder.log
# logs/auto_responder_error.log
```

## Testing

Test the background service:
```bash
python test_background_service.py
```

This will:
- Check if the service is running
- Test the health endpoint
- Send a test SMS webhook
- Verify auto-response functionality

## How It Works

1. **Background Process**: The service runs as a separate Python process
2. **Webhook Listener**: Listens on `http://localhost:5000/sms` for incoming SMS
3. **Auto-Response**: Generates and sends automatic replies via Textbelt
4. **Chat History**: Saves all conversations to JSON files
5. **Lead Tracking**: Updates lead status and conversation history

## Important Notes

⚠️ **Local Only**: The background service runs locally on your computer  
⚠️ **Heroku Webhook**: Your Textbelt webhook URL should point to your Heroku app  
⚠️ **API Keys**: Ensure your `.env` file has valid Textbelt and OpenAI keys  

## Troubleshooting

### Service Won't Start
1. Check if port 5000 is available
2. Verify environment variables are set
3. Check `logs/auto_responder_error.log` for details

### Not Receiving Responses
1. Verify Textbelt webhook URL is correct
2. Check if Heroku app is running: `https://your-app.herokuapp.com/webhook/health`
3. Test locally: `python test_background_service.py`

### Service Stops Unexpectedly
1. Check error logs: `logs/auto_responder_error.log`
2. Verify API quota isn't exhausted
3. Restart the service: `python run_background.py`

## File Structure

```
RE-Followup/
├── run_background.py          # Start service in background
├── stop_background.py         # Stop/check service status
├── start_service.bat         # Windows batch to start
├── stop_service.bat          # Windows batch to stop
├── install_startup.py        # Install auto-start
├── uninstall_startup.py      # Remove auto-start
├── test_background_service.py # Test service functionality
├── logs/
│   ├── auto_responder.log    # Service output logs
│   └── auto_responder_error.log # Error logs
└── auto_responder.pid        # Process ID file (when running)
```

## Security

- The service only listens on localhost (127.0.0.1)
- Webhook signature validation is implemented
- Logs don't contain sensitive API keys
- PID file tracks running processes

## Support

If you encounter issues:
1. Run `python test_background_service.py` for diagnostics
2. Check the log files in the `logs/` directory
3. Verify your environment variables are properly set
4. Test your Textbelt API key with `python test_sms.py` 