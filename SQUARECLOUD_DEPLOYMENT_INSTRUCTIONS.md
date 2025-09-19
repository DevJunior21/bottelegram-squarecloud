# Deploying to SquareCloud

## Prerequisites
1. Create an account at [SquareCloud](https://squarecloud.app)
2. Verify your email address
3. Have your Telegram Bot Token ready (from @BotFather on Telegram)

## Deployment Steps

### 1. Log in to SquareCloud
- Go to https://squarecloud.app and log in to your account

### 2. Create a New Application
- Click on "Create App" or "+" button
- Choose "Python" as your application type
- Select the appropriate plan for your needs (Free plan may be sufficient for testing)

### 3. Upload Your Application
- Upload the `bottelegram_squarecloud.zip` file that was created in the previous step
- The file is located at: `/root/bottelegram_squarecloud/bottelegram_squarecloud.zip`

### 4. Configure Application Settings
In the SquareCloud dashboard, configure the following settings:

- **Display Name**: BotTelegram
- **Description**: Bot Telegram com sistema de assinaturas e pagamentos
- **Memory**: 512 MB (as specified in your squarecloud.app file)
- **Version**: Python 18 (as specified in your squarecloud.app file)

### 5. Set Environment Variables
In the "Environment Variables" section, add the following variables:

```
SQUARECLOUD=true
DEBUG=false
DJANGO_SECRET_KEY=your_production_secret_key_here (generate a strong secret key)
DJANGO_ALLOWED_HOSTS=*

# Database settings (provided by SquareCloud when you add a database)
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=your_database_host
DATABASE_PORT=5432

# Redis settings (provided by SquareCloud when you add Redis)
REDIS_URL=redis://your-redis-host:6379/0

# Telegram Bot settings
TELEGRAM_BOT_TOKEN=your_actual_telegram_bot_token_here

# Optional settings (if you're using PushinPay)
PUSHINPAY_API_TOKEN=your_pushinpay_api_token
PUSHINGPAY_WEBHOOK_SECRET=your_webhook_secret
WEBHOOK_URL=https://your-app-id.squarecloud.app/webhook
```

### 6. Add Database and Redis (if needed)
- If your application requires a database, add a PostgreSQL database from the SquareCloud dashboard
- If your application uses Redis (for Celery), add a Redis service from the SquareCloud dashboard

### 7. Deploy the Application
- Click "Deploy" or "Start" to deploy your application
- Wait for the deployment process to complete

### 8. Run Initial Setup
After deployment, you may need to run initial setup commands:
1. Run migrations: `python manage.py migrate`
2. Collect static files: `python manage.py collectstatic --noinput`

These commands are already configured in your `squarecloud.app` startup command.

### 9. Configure Telegram Webhook (if needed)
If your bot uses webhooks instead of polling, you'll need to set up the webhook:
```
curl -F "url=https://your-app-id.squarecloud.app/telegram/webhook" https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook
```

## Troubleshooting Tips

1. **Check logs**: Use the SquareCloud dashboard to view your application logs
2. **Environment variables**: Ensure all required environment variables are set correctly
3. **Dependencies**: Make sure all dependencies in `requirements.txt` are compatible with SquareCloud
4. **Memory usage**: Monitor your application's memory usage and adjust if necessary

## Useful Commands for SquareCloud

These commands are already configured in your `squarecloud.app` file:
- Startup command: `python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT`

The `$PORT` environment variable is automatically provided by SquareCloud.