# 🐘 Configuração PostgreSQL na SquareCloud

## ✅ Correção Aplicada

O projeto foi ajustado para usar corretamente o banco PostgreSQL da SquareCloud.

### 🔧 **Mudanças Implementadas:**

1. **Adicionado `psycopg2-binary`** aos requirements
2. **Restaurado `dj-database-url`** para parsing da URL
3. **Configurado PostgreSQL via `DATABASE_URL`** no settings.py
4. **SQLite como fallback** para desenvolvimento local

### 🚀 **Como Configurar na SquareCloud:**

#### 1. **Variáveis de Ambiente Obrigatórias:**

No painel da SquareCloud, configure:

```env
DJANGO_SECRET_KEY=sua_chave_secreta_django_aqui
BOT_TOKEN=token_do_botfather_aqui
WEBHOOK_URL=https://SEU_SUBDOMINIO.squarecloud.app/webhook/
DATABASE_URL=postgresql://user:password@host:port/database
```

⚠️ **IMPORTANTE:** A `DATABASE_URL` será fornecida automaticamente pela SquareCloud quando você ativar o banco PostgreSQL no painel.

#### 2. **Como Obter a DATABASE_URL:**

1. No painel da SquareCloud, vá para sua aplicação
2. Acesse a seção **"Database"** ou **"PostgreSQL"**
3. Ative o banco PostgreSQL (pode ter custo adicional)
4. Copie a URL de conexão fornecida
5. Cole na variável de ambiente `DATABASE_URL`

#### 3. **Exemplo de DATABASE_URL:**

```
postgresql://squareuser:password123@pg-server.squarecloud.app:5432/database_name
```

### 📝 **Estrutura da Configuração:**

O arquivo `settings.py` agora funciona assim:

```python
# Se DATABASE_URL existir (SquareCloud PostgreSQL)
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL)
    }
# Senão, usar SQLite local (desenvolvimento)
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

### 🎯 **Deploy Atualizado:**

1. **Clone o repositório:**
```bash
git clone https://github.com/DevJunior21/bottelegram-squarecloud.git
cd bottelegram-squarecloud
```

2. **Prepare o deploy:**
```bash
./prepare_deploy.sh
```

3. **Configure as variáveis no painel SquareCloud:**
   - `DJANGO_SECRET_KEY`
   - `BOT_TOKEN`
   - `WEBHOOK_URL`
   - `DATABASE_URL` (fornecida pela SquareCloud)

4. **Upload do `bottelegram_deploy.zip`**

### 💰 **Custo do PostgreSQL:**

- Verifique os preços no painel da SquareCloud
- O PostgreSQL pode ter custo adicional
- SQLite local é gratuito para desenvolvimento

### 🔍 **Verificação:**

Após o deploy, verifique nos logs se aparece:
```
✅ Connecting to PostgreSQL database...
✅ Database connection successful
```

Em vez de erros de "psycopg2 module not found".

---

✅ **Agora o projeto está configurado corretamente para usar o PostgreSQL da SquareCloud!**