# BotTelegram para SquareCloud

Bot Telegram otimizado para deploy na plataforma SquareCloud.

## Estrutura do Projeto

```
bottelegram-squarecloud/
├── squarecloud.app          # Configuração do SquareCloud
├── requirements.txt         # Dependências do projeto
├── runtime.txt             # Versão do Python
├── .env.example            # Exemplo de variáveis de ambiente
├── manage.py               # Django management
├── core/                   # Configurações do Django
│   ├── settings.py         # Configurações otimizadas
│   ├── urls.py             # URLs principais
│   └── wsgi.py             # WSGI
├── bot_app/                # App do bot
│   ├── views.py            # Webhook views
│   ├── urls.py             # URLs do bot
│   └── management/         # Comandos de management
└── staticfiles/            # Arquivos estáticos
```

## Configuração

1. **Criar arquivo `.env`** a partir do `.env.example`:
   ```bash
   cp .env.example .env
   ```

2. **Configurar variáveis de ambiente** no arquivo `.env`:
   - `DJANGO_SECRET_KEY`: Chave secreta do Django
   - `BOT_TOKEN`: Token do bot do Telegram
   - `WEBHOOK_URL`: URL do webhook (https://seudominio.squarecloud.app/webhook/)

## Deploy na SquareCloud

1. **Criar aplicação** no painel da SquareCloud
2. **Fazer upload do projeto** (zip do diretório)
3. **Configurar variáveis de ambiente** no painel da SquareCloud
4. **Iniciar aplicação**

## Comandos Úteis

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Configurar webhook do Telegram
python manage.py setup_webhook

# Iniciar servidor de desenvolvimento
python manage.py runserver
```

## Variáveis de Ambiente Necessárias

Na SquareCloud, configure as seguintes variáveis de ambiente:

```
DJANGO_SECRET_KEY=sua_chave_secreta_aqui
DEBUG=False
ALLOWED_HOSTS=.squarecloud.app,localhost,127.0.0.1
BOT_TOKEN=seu_token_do_bot_aqui
DATABASE_URL=sqlite:///./db.sqlite3
REDIS_URL=redis://localhost:6379/0
WEBHOOK_URL=https://seudominio.squarecloud.app/webhook/
```

## Solução de Problemas

1. **Erro de dependências**: Verifique se todas as variáveis de ambiente estão configuradas
2. **Webhook não funciona**: Verifique se o `WEBHOOK_URL` está correto
3. **Problemas com permissões**: Verifique as configurações de `ALLOWED_HOSTS`

## Licença

MIT