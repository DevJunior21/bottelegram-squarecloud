displayName=BotTelegram
description=Bot Telegram com sistema de assinaturas e pagamentos
main=manage.py
memory=512
version=python20
startup=python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT