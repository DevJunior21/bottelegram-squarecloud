DISPLAY_NAME=BotTelegram
DESCRIPTION=Bot Telegram com sistema de assinaturas e pagamentos
SUBDOMAIN=bottelegram
MEMORY=512
VERSION=python-3.11
START=python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
INSTALL=pip install --upgrade pip && pip install -r requirements.txt