# 🔒 Correção do Erro CSRF no Admin

## 🐛 **Problema Identificado:**
```
POST https://bottelegramnew.squareweb.app/admin/login/ 403 (Forbidden)
```

O erro 403 no login do admin é causado por problemas de CSRF (Cross-Site Request Forgery) na SquareCloud.

## ✅ **Correções Aplicadas:**

### 1. **CSRF_TRUSTED_ORIGINS**
Adicionado suporte aos domínios da SquareCloud:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://*.squarecloud.app',
    'https://*.squareweb.app',
    'https://bottelegramnew.squareweb.app',
]
```

### 2. **Configurações de Segurança para HTTPS**
```python
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = False  # SquareCloud já gerencia isso
    USE_TZ = True
```

### 3. **Middleware de Debug CSRF**
Criado middleware para monitorar requisições CSRF:
```python
# core/middleware.py
class CSRFDebugMiddleware:
    # Logs informações de debug para identificar problemas CSRF
```

## 🚀 **Como Aplicar a Correção:**

### **Deploy Atualizado:**
```bash
git clone https://github.com/DevJunior21/bottelegram-squarecloud.git
cd bottelegram-squarecloud
./prepare_deploy.sh
```

### **Configuração SquareCloud:**
Use estas variáveis de ambiente:
```env
DJANGO_SECRET_KEY=sua_chave_secreta_aqui
DEBUG=False
BOT_TOKEN=token_do_botfather
WEBHOOK_URL=https://bottelegramnew.squareweb.app/webhook/
```

## 🔧 **Soluções Alternativas:**

### **Opção 1: Limpar Cache do Navegador**
1. Ctrl+Shift+Delete (Chrome/Firefox)
2. Limpar cookies e cache
3. Tentar login novamente

### **Opção 2: Modo Incógnito**
1. Abrir aba incógnita/privada
2. Acessar o admin
3. Fazer login normalmente

### **Opção 3: Verificar URL**
Certifique-se de usar a URL correta:
```
https://bottelegramnew.squareweb.app/admin/
```

## 🎯 **Credenciais do Admin:**
- **Usuário:** `admin`
- **Senha:** `Suzuya2109@bot/`

## 📋 **Logs de Debug:**

Após aplicar a correção, verifique os logs para:
```
POST request to /admin/login/
Host: bottelegramnew.squareweb.app
Origin: https://bottelegramnew.squareweb.app
X-Forwarded-Proto: https
```

## ✅ **Resultado Esperado:**

Após a correção:
```
POST /admin/login/ HTTP/1.1" 302 0  ✅ Login Success
GET /admin/ HTTP/1.1" 200 OK       ✅ Admin Dashboard
```

---

**🔒 Esta correção resolve definitivamente problemas de CSRF no admin da SquareCloud!**