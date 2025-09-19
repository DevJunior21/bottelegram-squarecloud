# CONFIGURAÇÃO CORRETA DAS VARIÁVEIS DE AMBIENTE

## Importante:
As variáveis de ambiente que contêm caracteres especiais (como +, $, &, etc.) DEVEM ser colocadas entre aspas duplas.

## Variáveis obrigatórias:

SQUARECLOUD=true
DEBUG=false
DJANGO_SECRET_KEY="django-insecure-8a@#b2z$5r%9w!e3q7u*4t1y6i&o0p_l-m+nkjhgfdsazxcvbnm"
DJANGO_ALLOWED_HOSTS="*"

## Variáveis do banco de dados (se usar PostgreSQL):
DATABASE_NAME=seu_banco_de_dados
DATABASE_USER=seu_usuario
DATABASE_PASSWORD="sua_senha_segura"
DATABASE_HOST=endereco_do_servidor
DATABASE_PORT=5432

## Variáveis do Redis (se usar):
REDIS_URL="redis://endereco:6379/0"

## Token do Telegram (obrigatório):
TELEGRAM_BOT_TOKEN=seu_token_aqui

## Variáveis opcionais (se usar PushinPay):
PUSHINPAY_API_TOKEN=seu_token_api
PUSHINGPAY_WEBHOOK_SECRET=sua_chave_secreta
WEBHOOK_URL="https://seu-app.squarecloud.app/webhook"

## Erros comuns:
1. Esquecer as aspas em valores com caracteres especiais
2. Usar espaços em torno do sinal de igual (=)
3. Não definir todas as variáveis obrigatórias