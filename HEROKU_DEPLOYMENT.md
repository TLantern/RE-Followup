# Heroku Deployment Guide for SMS Auto-Responder

This guide will walk you through deploying your SMS Auto-Responder application to Heroku.

## Prerequisites

1. A [Heroku account](https://signup.heroku.com/)
2. [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) installed
3. Git installed on your machine
4. Your Textbelt API key

## Step 1: Prepare Your Application

The application is already set up for Heroku deployment with:
- `Procfile` - Tells Heroku how to run the application
- `runtime.txt` - Specifies the Python version
- `requirements.txt` - Lists all dependencies

## Step 2: Create a Heroku App

```bash
# Login to Heroku
heroku login

# Create a new Heroku app
heroku create your-app-name
```

Replace `your-app-name` with a unique name for your application.

## Step 3: Configure Environment Variables

Set up your environment variables on Heroku:

```bash
heroku config:set TEXTBELT_API_KEY=your_textbelt_api_key --app your-app-name
heroku config:set TEXTBELT_WEBHOOK_URL=https://your-app-name.herokuapp.com/sms --app your-app-name
heroku config:set OPENAI_API_KEY=your_openai_api_key --app your-app-name
```

## Step 4: Deploy to Heroku

```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit for Heroku deployment"

# Add Heroku as a remote
heroku git:remote -a your-app-name

# Push to Heroku
git push heroku main
```

## Step 5: Update Webhook URL

After deployment, update your Textbelt webhook URL to point to your Heroku app:

```bash
python update_heroku_webhook.py your-app-name
```

## Step 6: Verify Deployment

1. Check if the app is running:
   ```bash
   heroku open --app your-app-name
   ```

2. Test the webhook health endpoint:
   ```bash
   curl https://your-app-name.herokuapp.com/webhook/health
   ```

3. View logs:
   ```bash
   heroku logs --tail --app your-app-name
   ```

## Troubleshooting

### Application Error

If you see an "Application Error" page:
1. Check the logs: `heroku logs --tail --app your-app-name`
2. Ensure all environment variables are set correctly
3. Verify that the Procfile is correctly formatted

### Port Binding Error

If you see a port binding error:
1. Make sure your app is using the PORT environment variable provided by Heroku
2. Check that `main.py` is correctly configured to use `os.getenv('PORT', 8080)`

### Webhook Not Working

If your webhook isn't receiving messages:
1. Verify the webhook URL in your Textbelt account
2. Check that the webhook URL is correctly formatted as `https://your-app-name.herokuapp.com/sms`
3. Test the webhook endpoint manually

## Scaling

By default, Heroku deploys your app with one web dyno. You can scale as needed:

```bash
# Scale to more dynos
heroku ps:scale web=2 --app your-app-name

# Scale down to save dyno hours
heroku ps:scale web=1 --app your-app-name
```

## Maintenance

### Updating Your App

After making changes to your code:

```bash
git add .
git commit -m "Update description"
git push heroku main
```

### Restarting Your App

If needed, you can restart your app:

```bash
heroku restart --app your-app-name
``` 