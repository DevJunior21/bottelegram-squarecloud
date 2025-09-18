#!/bin/bash

# Script para criar repositório no GitHub via API

# Verificar se GITHUB_TOKEN está configurado
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Por favor, defina a variável de ambiente GITHUB_TOKEN com seu GitHub Personal Access Token"
    echo "Exemplo: export GITHUB_TOKEN=seu_token_aqui"
    exit 1
fi

# Configurações
USERNAME="DevJunior21"
REPO_NAME="bottelegram-squarecloud"
DESCRIPTION="Bot Telegram otimizado para SquareCloud"
PRIVATE=false

# Criar repositório via API do GitHub
echo "Criando repositório $REPO_NAME no GitHub..."

RESPONSE=$(curl -s -w "%{http_code}" -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/user/repos \
  -d "{
    \"name\": \"$REPO_NAME\",
    \"description\": \"$DESCRIPTION\",
    \"private\": $PRIVATE,
    \"auto_init\": false
  }")

HTTP_CODE=${RESPONSE: -3}
RESPONSE_BODY=${RESPONSE%???}

if [ "$HTTP_CODE" -eq "201" ]; then
    echo "✅ Repositório criado com sucesso!"
    echo "URL: https://github.com/$USERNAME/$REPO_NAME"
    
    # Adicionar remote e fazer push
    echo "Configurando remote e fazendo push..."
    cd /root/bottelegram_squarecloud
    git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git"
    
    # Verificar se há commits para enviar
    if [ "$(git rev-parse --verify HEAD 2>/dev/null)" ]; then
        git push -u origin main || git push -u origin master
    else
        echo "Nenhum commit encontrado para enviar"
    fi
    
elif [ "$HTTP_CODE" -eq "422" ]; then
    echo "⚠️  Repositório já existe ou há um problema com as configurações"
    echo "Detalhes: $RESPONSE_BODY"
    
    # Tentar adicionar remote mesmo assim
    cd /root/bottelegram_squarecloud
    git remote add origin "https://github.com/$USERNAME/$REPO_NAME.git" 2>/dev/null || true
    git push -u origin main || git push -u origin master
else
    echo "❌ Erro ao criar repositório. Código HTTP: $HTTP_CODE"
    echo "Detalhes: $RESPONSE_BODY"
    exit 1
fi