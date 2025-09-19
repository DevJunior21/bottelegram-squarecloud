# 📋 Guia Completo de Configuração na SquareCloud

## 🔗 Repositório GitHub
**Link:** https://github.com/DevJunior21/bottelegram-squarecloud.git

## 🚀 Passos para Deploy na SquareCloud

### 1. 📥 Download do Projeto

```bash
git clone https://github.com/DevJunior21/bottelegram-squarecloud.git
cd bottelegram-squarecloud
```

### 2. 🎯 Preparação para Deploy

Execute o script de preparação:
```bash
./prepare_deploy.sh
```

Isso irá gerar o arquivo `bottelegram_deploy.zip` otimizado para a SquareCloud.

### 3. 🌐 Configuração na SquareCloud

#### A. Acesse o Painel da SquareCloud
1. Vá para https://squarecloud.app/
2. Faça login na sua conta
3. Clique em "Criar Nova Aplicação"

#### B. Upload do Projeto
1. Selecione o arquivo `bottelegram_deploy.zip`
2. Aguarde o upload completo

#### C. Configurar Variáveis de Ambiente

No painel da SquareCloud, na seção **Environment Variables**, adicione:

```env
DJANGO_SECRET_KEY=sua_chave_secreta_django_super_segura_aqui
DEBUG=False
ALLOWED_HOSTS=.squarecloud.app,localhost,127.0.0.1
BOT_TOKEN=seu_token_do_bot_telegram_do_botfather
WEBHOOK_URL=https://bottelegram.squarecloud.app/webhook/
```

### 4. 🔑 Como Obter as Variáveis

#### BOT_TOKEN
1. Abra o Telegram
2. Procure por `@BotFather`
3. Digite `/newbot` para criar um novo bot
4. Siga as instruções e copie o token fornecido

#### DJANGO_SECRET_KEY
Use um gerador online ou execute em Python:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### WEBHOOK_URL
Substitua `bottelegram` pelo subdomínio escolhido na SquareCloud:
```
https://SEU_SUBDOMINIO.squarecloud.app/webhook/
```

### 5. 🚀 Iniciar Aplicação

1. Clique em **"Start"** no painel da SquareCloud
2. Aguarde o build e deploy (pode levar alguns minutos)
3. Verifique os logs em tempo real

### 6. ⚙️ Configurar Webhook do Telegram

Após o deploy bem-sucedido:

1. Acesse o **Terminal** da aplicação no painel da SquareCloud
2. Execute:
```bash
python manage.py setup_webhook
```
3. Você deve ver: "Webhook configurado com sucesso!"

### 7. ✅ Testar o Bot

1. Abra o Telegram
2. Procure pelo seu bot (nome definido no BotFather)
3. Digite `/start` para testar

### 8. 🔧 Administração Django

Acesse o painel admin em:
```
https://SEU_SUBDOMINIO.squarecloud.app/admin/
```

**Credenciais padrão:**
- Usuário: `admin`
- Senha: `Suzuya2109@bot/`

⚠️ **IMPORTANTE:** Altere a senha após o primeiro login!

## 🐛 Solução de Problemas

### Bot não responde:
1. Verifique se o `BOT_TOKEN` está correto
2. Execute `python manage.py setup_webhook` novamente
3. Confirme que o `WEBHOOK_URL` está correto

### Erro de deploy:
1. Verifique se todas as variáveis de ambiente estão configuradas
2. Veja os logs no painel da SquareCloud
3. Confirme que o arquivo ZIP foi gerado corretamente

### Erro de memória:
- Aumente a memória no arquivo `squarecloud.app` (ex: MEMORY=1024)

### Webhook já configurado em outro servidor:
1. Execute no terminal:
```bash
python manage.py shell
>>> import requests
>>> requests.post(f"https://api.telegram.org/bot{SEU_TOKEN}/deleteWebhook")
```
2. Depois execute `python manage.py setup_webhook`

## 📂 Estrutura do Projeto no Deploy

```
bottelegram-squarecloud/
├── core/                   # Configurações Django
├── bot_app/               # App principal do bot
├── staticfiles/           # Arquivos estáticos
├── manage.py             # Django management
├── squarecloud.app       # Configuração SquareCloud
├── requirements.txt      # Dependências
└── DEPLOY_SQUARECLOUD.md # Instruções técnicas
```

## 🎯 Próximos Passos

Após o deploy bem-sucedido:
1. Personalize as respostas do bot em `bot_app/views.py`
2. Adicione novos comandos
3. Configure integrações (se necessário)
4. Monitore os logs regularmente

---

✅ **O projeto está pronto para produção na SquareCloud!**