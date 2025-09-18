#!/usr/bin/env python3
"""
Script para auxiliar na configuração do repositório GitHub
"""

import os
import sys
import subprocess
import json

def check_git_installed():
    """Verifica se o Git está instalado"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_git_config():
    """Obtém as configurações do Git"""
    try:
        username = subprocess.run(["git", "config", "user.name"], capture_output=True, text=True).stdout.strip()
        email = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True).stdout.strip()
        return username, email
    except subprocess.CalledProcessError:
        return None, None

def check_github_token():
    """Verifica se o token do GitHub está configurado"""
    return os.environ.get('GITHUB_TOKEN')

def create_repo_instructions():
    """Cria instruções para criar repositório no GitHub"""
    instructions = """
===============================
CONFIGURAÇÃO DO GITHUB
===============================

📝 PASSO 1: CRIAR TOKEN NO GITHUB
---------------------------------
1. Acesse: https://github.com/settings/tokens
2. Clique em "Generate new token"
3. Dê um nome (ex: "BotTelegram SquareCloud")
4. Selecione a permissão "repo" (full control)
5. Clique em "Generate token"
6. COPIE O TOKEN GERADO (ele não aparecerá novamente)

🔐 PASSO 2: CONFIGURAR TOKEN
----------------------------
No terminal, execute:
export GITHUB_TOKEN=cole_seu_token_aqui

🔁 PASSO 3: EXECUTAR SCRIPT
---------------------------
chmod +x create_github_repo.sh
./create_github_repo.sh

✅ VERIFICAÇÃO
-------------
Após concluir, acesse:
https://github.com/seu-usuario/bottelegram-squarecloud

Se encontrar problemas, execute:
python3 setup_github.py troubleshoot
    """
    return instructions

def troubleshoot():
    """Função de diagnóstico"""
    print("🔍 DIAGNÓSTICO DO AMBIENTE")
    print("=" * 40)
    
    # Verificar Git
    if check_git_installed():
        print("✅ Git: Instalado")
    else:
        print("❌ Git: Não encontrado")
        print("   Instale com: sudo apt install git")
        return
    
    # Verificar configurações do Git
    username, email = get_git_config()
    if username and email:
        print(f"✅ Git Config: {username} <{email}>")
    else:
        print("⚠️  Git Config: Não configurado")
        print("   Configure com:")
        print("   git config --global user.name \"Seu Nome\"")
        print("   git config --global user.email \"seu@email.com\"")
    
    # Verificar token
    token = check_github_token()
    if token:
        print("✅ GitHub Token: Configurado")
        print("   (mantenha este token seguro)")
    else:
        print("❌ GitHub Token: Não configurado")
        print("   Defina com: export GITHUB_TOKEN=seu_token")
    
    # Verificar repositório local
    try:
        result = subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, text=True, cwd="/root/bottelegram_squarecloud")
        if result.returncode == 0:
            print("✅ Repositório Local: Configurado")
            
            # Verificar commits
            result = subprocess.run(["git", "log", "--oneline", "-1"], capture_output=True, text=True, cwd="/root/bottelegram_squarecloud")
            if result.returncode == 0 and result.stdout.strip():
                print("✅ Commits Locais: Encontrados")
            else:
                print("⚠️  Commits Locais: Nenhum encontrado")
                
            # Verificar remote
            result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True, cwd="/root/bottelegram_squarecloud")
            if "origin" in result.stdout:
                print("✅ Remote Configurado: Sim")
                print(f"   URL: {result.stdout.split()[1]}")
            else:
                print("❌ Remote Configurado: Não")
        else:
            print("❌ Repositório Local: Não encontrado")
    except Exception as e:
        print(f"❌ Erro ao verificar repositório: {e}")

def main():
    """Função principal"""
    if len(sys.argv) > 1 and sys.argv[1] == "troubleshoot":
        troubleshoot()
        return
    
    print(create_repo_instructions())
    
    # Oferecer ajuda adicional
    print("\n💡 DICAS ADICIONAIS:")
    print("- Para verificar configurações: python3 setup_github.py troubleshoot")
    print("- Para ver commits locais: git log --oneline")
    print("- Para ver arquivos não versionados: git status")
    print("- Para forçar push: git push -f origin main")

if __name__ == "__main__":
    main()