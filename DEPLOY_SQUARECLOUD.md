# Deploy na SquareCloud - Instruções Corrigidas

## Problemas Identificados e Correções

### 1. Erro no arquivo .env
**Problema:** Linha 5 com sintaxe incorreta
**Solução:** Arquivo .env.squarecloud foi simplificado

### 2. Erro de configuração do banco de dados
**Problema:** Django tentava usar PostgreSQL sem configuração
**Solução:** Configurado para usar SQLite por padrão

## Arquivos Corrigidos

1. **core/settings.py**
   - Removido Celery/Redis (não necessário inicialmente)
   - Banco de dados configurado para SQLite por padrão
   - Configuração simplificada

2. **requirements.txt**
   - Removidas dependências desnecessárias
   - Mantidas apenas as essenciais

3. **squarecloud.app**
   - Comando START simplificado
   - Removido comando create_admin

4. **.env.squarecloud**
   - Formato correto sem erros de sintaxe
   - Variáveis essenciais apenas

## Como fazer o Deploy

### Passo 1: Preparar o projeto
```bash
cd /root/bottelegram_squarecloud
./prepare_deploy.sh
```

### Passo 2: Configurar variáveis no painel da SquareCloud

No painel da SquareCloud, adicione estas variáveis de ambiente:

```
DJANGO_SECRET_KEY=gere_uma_chave_secreta_segura_aqui
DEBUG=False
ALLOWED_HOSTS=.squarecloud.app
BOT_TOKEN=seu_token_do_bot_telegram
WEBHOOK_URL=https://bottelegram.squarecloud.app/webhook/
```

### Passo 3: Upload do projeto

1. Use o arquivo `bottelegram_deploy.zip` gerado
2. Faça upload no painel da SquareCloud
3. Aguarde o build e deploy

### Passo 4: Configurar Webhook (após deploy)

Acesse o terminal da aplicação na SquareCloud e execute:
```bash
python manage.py setup_webhook
```

## Variáveis de Ambiente Obrigatórias

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| DJANGO_SECRET_KEY | Chave secreta do Django | Use um gerador de chaves |
| BOT_TOKEN | Token do bot do Telegram | Obtido do @BotFather |
| WEBHOOK_URL | URL do webhook | https://SEU_APP.squarecloud.app/webhook/ |

## Solução de Problemas

### Se o deploy falhar:

1. **Verifique os logs** no painel da SquareCloud
2. **Confirme que o BOT_TOKEN** está correto
3. **Verifique se a memória** (512MB) é suficiente
4. **Teste localmente** primeiro:
   ```bash
   python manage.py runserver
   ```

### Se o bot não responder:

1. Execute `python manage.py setup_webhook` no terminal
2. Verifique se o WEBHOOK_URL está correto
3. Confirme que o bot não está em uso em outro servidor

## Estrutura Simplificada

O projeto foi simplificado para o deploy inicial:
- Usando SQLite (sem necessidade de PostgreSQL)
- Sem Celery/Redis (adicionar quando necessário)
- Configuração mínima funcional

Após o deploy bem-sucedido, você pode adicionar funcionalidades gradualmente.