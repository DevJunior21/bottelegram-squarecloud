#!/bin/bash

echo "Preparando projeto para deploy na SquareCloud..."

# Criar banco de dados local
echo "Criando banco de dados..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Criar arquivo ZIP para deploy
echo "Criando arquivo ZIP para deploy..."
zip -r bottelegram_deploy.zip . \
    -x "*.pyc" \
    -x "__pycache__/*" \
    -x "venv/*" \
    -x ".git/*" \
    -x ".gitignore" \
    -x "*.sqlite3" \
    -x "*.log" \
    -x "prepare_deploy.sh"

echo "Arquivo bottelegram_deploy.zip criado com sucesso!"
echo ""
echo "INSTRUÇÕES PARA DEPLOY:"
echo "1. Faça upload do arquivo bottelegram_deploy.zip na SquareCloud"
echo "2. Configure as variáveis de ambiente no painel da SquareCloud:"
echo "   - DJANGO_SECRET_KEY: Gere uma chave secreta segura"
echo "   - BOT_TOKEN: Token do seu bot do Telegram"
echo "   - WEBHOOK_URL: https://SEU_SUBDOMINIO.squarecloud.app/webhook/"
echo "3. Inicie a aplicação"