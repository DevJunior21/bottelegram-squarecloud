# 🔑 Variáveis de Ambiente Completas

## ✅ **Variáveis OBRIGATÓRIAS para SquareCloud:**

### **1. Django (Obrigatórias)**
```env
DJANGO_SECRET_KEY=sua_chave_secreta_django_super_segura_aqui
BOT_TOKEN=token_do_bot_do_telegram_do_botfather
```

### **2. Webhook (Obrigatória)**
```env
WEBHOOK_URL=https://bottelegramnew.squareweb.app/webhook/
```

## ⚠️ **Variáveis da PushinPay (Para Pagamentos PIX):**

### **Status: ✅ CONFIGURADA NO PROJETO**

```env
PUSHINPAY_API_TOKEN=seu_token_api_pushinpay_aqui
PUSHINGPAY_WEBHOOK_SECRET=sua_chave_secreta_webhook_pushinpay
```

**🔧 Como Obter:**
1. Acesse https://pushinpay.com.br/
2. Crie uma conta
3. Vá em **API/Integrações**
4. Copie o **API Token**
5. Configure o **Webhook Secret**

**⚠️ Importante:**
- **SEM essas variáveis:** Sistema funciona em **MODO TESTE**
- **COM essas variáveis:** PIX real funcionando

## 🔧 **Variáveis Opcionais:**

### **3. Banco PostgreSQL (Opcional - Pago)**
```env
DATABASE_URL=postgresql://user:password@host:port/database
```
*Se não configurar: usa SQLite (gratuito)*

### **4. Grupo Telegram (Opcional)**
```env
TELEGRAM_GROUP_ID=id_do_grupo_telegram_para_notificacoes
```

### **5. Redis/Celery (Opcional)**
```env
REDIS_URL=redis://localhost:6379/0
```
*Para automação de promoções*

## 🚀 **Configuração na SquareCloud:**

### **Mínimo Funcional (3 variáveis):**
```env
DJANGO_SECRET_KEY=chave_secreta_aqui
BOT_TOKEN=token_do_bot
WEBHOOK_URL=https://bottelegramnew.squareweb.app/webhook/
```

### **Completo com PIX (5 variáveis):**
```env
DJANGO_SECRET_KEY=chave_secreta_aqui
BOT_TOKEN=token_do_bot
WEBHOOK_URL=https://bottelegramnew.squareweb.app/webhook/
PUSHINPAY_API_TOKEN=token_pushinpay
PUSHINGPAY_WEBHOOK_SECRET=secret_webhook
```

## 📋 **Status da PushinPay:**

### ✅ **TOTALMENTE CONFIGURADA**
- ✅ Arquivo `integrations/pushingpay.py` - API completa
- ✅ Arquivo `integrations/pushingpay_webhook.py` - Webhook seguro
- ✅ Modelo `Pagamento` com campos PushinPay
- ✅ Sistema de PIX automático
- ✅ Modo teste quando não configurado

### 🔧 **Funcionalidades PIX:**
1. **Criação de cobrança PIX**
2. **QR Code automático**
3. **Código copia e cola**
4. **Webhook de confirmação**
5. **Verificação de assinatura**
6. **Modo teste integrado**

## 🎯 **Como Funciona:**

### **Com PushinPay Configurada:**
1. Usuário escolhe plano
2. Sistema gera PIX real
3. QR code e copia-cola funcionais
4. Webhook confirma pagamento
5. Assinatura ativada automaticamente

### **Sem PushinPay (Modo Teste):**
1. Usuário escolhe plano
2. Sistema gera PIX de teste
3. Mensagem indica "MODO DE TESTE"
4. Admin pode ativar manualmente

## 🔗 **URLs de Webhook:**

### **Telegram:**
```
https://bottelegramnew.squareweb.app/webhook/
```

### **PushinPay:**
```
https://bottelegramnew.squareweb.app/webhook/pushinpay/
```

## 📊 **Resumo:**

| Variável | Status | Obrigatória | Função |
|----------|--------|-------------|---------|
| DJANGO_SECRET_KEY | ✅ | Sim | Segurança Django |
| BOT_TOKEN | ✅ | Sim | Bot Telegram |
| WEBHOOK_URL | ✅ | Sim | Webhook Telegram |
| PUSHINPAY_API_TOKEN | ✅ | Não* | PIX real |
| PUSHINGPAY_WEBHOOK_SECRET | ✅ | Não* | Segurança PIX |
| DATABASE_URL | ✅ | Não | PostgreSQL |
| TELEGRAM_GROUP_ID | ✅ | Não | Notificações |
| REDIS_URL | ✅ | Não | Automação |

*Obrigatória apenas se quiser PIX real funcionando

---

## ✅ **RESULTADO:**
**A PushinPay está 100% configurada no projeto! Configure as variáveis para ativar pagamentos PIX reais.**