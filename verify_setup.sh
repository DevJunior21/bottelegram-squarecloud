#!/bin/bash

echo "🔍 VERIFICAÇÃO DO AMBIENTE"
echo "==========================="

# Verificar se estamos no diretório correto
if [ ! -d "/root/bottelegram_squarecloud" ]; then
    echo "❌ Diretório do projeto não encontrado"
    exit 1
fi

cd /root/bottelegram_squarecloud

echo "✅ Diretório do projeto: OK"

# Verificar Git
if ! command -v git &> /dev/null; then
    echo "❌ Git não está instalado"
    exit 1
fi

echo "✅ Git: Instalado"

# Verificar se é um repositório Git
if [ ! -d ".git" ]; then
    echo "❌ Não é um repositório Git"
    exit 1
fi

echo "✅ Repositório Git: Configurado"

# Verificar commits
COMMITS_COUNT=$(git rev-list --count HEAD)
if [ "$COMMITS_COUNT" -gt 0 ]; then
    echo "✅ Commits locais: $COMMITS_COUNT"
else
    echo "❌ Nenhum commit encontrado"
fi

# Verificar arquivos essenciais
ESSENTIAL_FILES=("manage.py" "requirements.txt" "squarecloud.app" "README.md" "GITHUB_SETUP.md")
for file in "${ESSENTIAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ Arquivo essencial: $file"
    else
        echo "❌ Arquivo essencial ausente: $file"
    fi
done

# Verificar diretórios essenciais
ESSENTIAL_DIRS=("core" "bot" "tasks" "integrations" "promocoes" "carrossel" "welcome")
for dir in "${ESSENTIAL_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ Diretório essencial: $dir"
    else
        echo "❌ Diretório essencial ausente: $dir"
    fi
done

# Verificar scripts auxiliares
SCRIPTS=("create_github_repo.sh" "setup_github.py")
for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "✅ Script auxiliar: $script"
    else
        echo "❌ Script auxiliar ausente: $script"
    fi
done

# Verificar permissões dos scripts
if [ -x "create_github_repo.sh" ] && [ -x "setup_github.py" ]; then
    echo "✅ Permissões dos scripts: OK"
else
    echo "⚠️  Permissões dos scripts: Precisam ser ajustadas"
    echo "   Execute: chmod +x create_github_repo.sh setup_github.py"
fi

# Verificar arquivos estáticos
if [ -d "static" ] && [ -n "$(ls -A static)" ]; then
    STATIC_COUNT=$(find static -type f | wc -l)
    echo "✅ Arquivos estáticos: $STATIC_COUNT arquivos"
else
    echo "❌ Arquivos estáticos: Não encontrados"
fi

echo ""
echo "📋 RESUMO"
echo "========="

# Mostrar últimos commits
echo "Últimos commits:"
git log --oneline -3

echo ""
echo "📁 Status atual:"
git status --porcelain | wc -l | xargs -I {} echo "  Arquivos não versionados: {}"

echo ""
echo "🔧 PRÓXIMOS PASSOS:"
echo "1. Siga as instruções em GITHUB_SETUP.md"
echo "2. Exporte seu token GitHub: export GITHUB_TOKEN=seu_token"
echo "3. Execute: ./create_github_repo.sh"
echo ""
echo "Para ajuda adicional: python3 setup_github.py troubleshoot"