DISPLAY_NAME=Bot Telegram Django
DESCRIPTION=Bot Telegram com Django
SUBDOMAIN=bottelegram
MEMORY=512
VERSION=python-3.11
START=python manage.py makemigrations bot_app --noinput && python manage.py migrate --noinput && python manage.py create_admin && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:$PORT
INSTALL=pip install --upgrade pip && pip install -r requirements.txt
