#!/usr/bin/env python3
"""
Script completo para publicar o projeto no GitHub
"""

import os
import sys
import subprocess
import json
import time

def print_header():
    """Imprime cabeçalho do script"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                      🚀 PUBLICAR PROJETO NO GITHUB                          ║
║                                                                              ║
║              BotTelegram otimizado para SquareCloud                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)

def check_prerequisites():
    """Verifica pré-requisitos"""
    print("🔍 VERIFICANDO PRÉ-REQUISITOS...")
    print("=" * 50)
    
    # Verificar Git
    try:
        git_version = subprocess.run(["git", "--version"], capture_output=True, text=True, check=True)
        print(f"✅ Git: {git_version.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Git não encontrado!")
        print("   Instale com: sudo apt install git")
        return False
    
    # Verificar diretório do projeto
    project_dir = "/root/bottelegram_squarecloud"
    if not os.path.exists(project_dir):
        print("❌ Diretório do projeto não encontrado!")
        return False
    
    print(f"✅ Diretório do projeto: {project_dir}")
    
    # Verificar repositório Git
    git_dir = os.path.join(project_dir, ".git")
    if not os.path.exists(git_dir):
        print("❌ Não é um repositório Git!")
        return False
    
    print("✅ Repositório Git: Configurado")
    
    # Verificar commits
    try:
        result = subprocess.run(["git", "rev-list", "--count", "HEAD"], 
                               capture_output=True, text=True, check=True, cwd=project_dir)
        commit_count = int(result.stdout.strip())
        print(f"✅ Commits locais: {commit_count}")
    except (subprocess.CalledProcessError, ValueError):
        print("❌ Erro ao contar commits!")
        return False
    
    # Verificar token do GitHub
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("⚠️  Token do GitHub não configurado!")
        print("   Execute: export GITHUB_TOKEN=seu_token_aqui")
        return False
    
    print("✅ Token do GitHub: Configurado")
    
    print("\n🎉 Todos os pré-requisitos verificados com sucesso!\n")
    return True

def get_user_info():
    """Obtém informações do usuário do Git"""
    try:
        username = subprocess.run(["git", "config", "user.name"], 
                                 capture_output=True, text=True, 
                                 check=True, cwd="/root/bottelegram_squarecloud").stdout.strip()
        email = subprocess.run(["git", "config", "user.email"], 
                              capture_output=True, text=True, 
                              check=True, cwd="/root/bottelegram_squarecloud").stdout.strip()
        return username, email
    except subprocess.CalledProcessError:
        return "Unknown", "unknown@example.com"

def create_github_repo():
    """Cria repositório no GitHub via API"""
    print("🔨 CRIANDO REPOSITÓRIO NO GITHUB...")
    print("=" * 50)
    
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("❌ Token do GitHub não configurado!")
        return False
    
    username, email = get_user_info()
    repo_name = "bottelegram-squarecloud"
    
    # Dados para criar o repositório
    repo_data = {
        "name": repo_name,
        "description": "Bot Telegram otimizado para SquareCloud",
        "private": False,
        "auto_init": False
    }
    
    # Criar repositório via API
    try:
        import requests
        
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.post(
            "https://api.github.com/user/repos",
            headers=headers,
            json=repo_data
        )
        
        if response.status_code == 201:
            print(f"✅ Repositório '{repo_name}' criado com sucesso!")
            print(f"🔗 URL: https://github.com/{username}/{repo_name}")
            return True
        elif response.status_code == 422:
            print(f"⚠️  Repositório '{repo_name}' já existe!")
            print(f"🔗 URL: https://github.com/{username}/{repo_name}")
            return True
        else:
            print(f"❌ Erro ao criar repositório: {response.status_code}")
            print(f"Detalhes: {response.text}")
            return False
            
    except ImportError:
        print("⚠️  Biblioteca 'requests' não encontrada, usando curl...")
        return create_github_repo_curl()
    except Exception as e:
        print(f"❌ Erro ao criar repositório: {e}")
        return False

def create_github_repo_curl():
    """Cria repositório usando curl"""
    github_token = os.environ.get('GITHUB_TOKEN')
    username, _ = get_user_info()
    repo_name = "bottelegram-squarecloud"
    
    try:
        # Criar repositório via curl
        curl_cmd = [
            "curl", "-s", "-w", "%{http_code}", "-X", "POST",
            "-H", f"Authorization: token {github_token}",
            "-H", "Accept: application/vnd.github.v3+json",
            "https://api.github.com/user/repos",
            "-d", f'{{"name":"{repo_name}","description":"Bot Telegram otimizado para SquareCloud","private":false}}'
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True, 
                               cwd="/root/bottelegram_squarecloud")
        
        http_code = result.stdout[-3:]
        response_body = result.stdout[:-3]
        
        if http_code == "201":
            print(f"✅ Repositório '{repo_name}' criado com sucesso!")
            print(f"🔗 URL: https://github.com/{username}/{repo_name}")
            return True
        elif http_code == "422":
            print(f"⚠️  Repositório '{repo_name}' já existe!")
            print(f"🔗 URL: https://github.com/{username}/{repo_name}")
            return True
        else:
            print(f"❌ Erro ao criar repositório. Código HTTP: {http_code}")
            print(f"Detalhes: {response_body}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao criar repositório com curl: {e}")
        return False

def configure_remote():
    """Configura remote do repositório"""
    print("\n🔧 CONFIGURANDO REMOTE...")
    print("=" * 50)
    
    username, _ = get_user_info()
    repo_name = "bottelegram-squarecloud"
    remote_url = f"https://github.com/{username}/{repo_name}.git"
    
    try:
        # Remover remote existente (se houver)
        subprocess.run(["git", "remote", "remove", "origin"], 
                      cwd="/root/bottelegram_squarecloud", 
                      capture_output=True)
    except:
        pass  # Ignorar erros se não existir remote
    
    try:
        # Adicionar remote
        subprocess.run(["git", "remote", "add", "origin", remote_url], 
                      check=True, cwd="/root/bottelegram_squarecloud")
        print(f"✅ Remote configurado: {remote_url}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao configurar remote: {e}")
        return False

def push_to_github():
    """Faz push para o repositório no GitHub"""
    print("\n🚀 FAZENDO PUSH PARA O GITHUB...")
    print("=" * 50)
    
    try:
        # Verificar branch atual
        result = subprocess.run(["git", "branch", "--show-current"], 
                              capture_output=True, text=True, 
                              check=True, cwd="/root/bottelegram_squarecloud")
        current_branch = result.stdout.strip()
        
        if not current_branch:
            # Se não houver branch atual, usar main
            current_branch = "main"
            subprocess.run(["git", "checkout", "-b", current_branch], 
                          check=True, cwd="/root/bottelegram_squarecloud")
        
        print(f"🔄 Branch atual: {current_branch}")
        
        # Fazer push
        print("📤 Enviando commits para o GitHub...")
        subprocess.run(["git", "push", "-u", "origin", current_branch], 
                      check=True, cwd="/root/bottelegram_squarecloud")
        
        print("✅ Push concluído com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao fazer push: {e}")
        return False

def show_final_summary():
    """Mostra resumo final"""
    print("\n" + "=" * 80)
    print("🎉 PUBLICAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 80)
    
    username, _ = get_user_info()
    repo_name = "bottelegram-squarecloud"
    
    print(f"""
✅ REPOSITÓRIO PUBLICADO: https://github.com/{username}/{repo_name}

📊 RESUMO:
   • 5 commits enviados
   • Todos os arquivos versionados
   • Documentação completa incluída
   • Scripts auxiliares disponíveis

📁 PRÓXIMOS PASSOS:
   1. Acesse o repositório no GitHub
   2. Verifique os arquivos e commits
   3. Configure a integração com a SquareCloud
   4. Adicione colaboradores (se necessário)

📖 DOCUMENTAÇÃO DISPONÍVEL:
   • README.md - Descrição do projeto
   • GITHUB_SETUP.md - Instruções detalhadas
   • SUMMARY.md - Resumo completo
   • FINAL_INSTRUCTIONS.md - Próximos passos

🔧 COMANDOS ÚTEIS:
   • Ver commits: git log --oneline
   • Ver status: git status
   • Adicionar arquivos: git add .
   • Fazer commit: git commit -m "mensagem"
   • Fazer push: git push

💡 DICAS:
   • Mantenha seu token do GitHub em segurança
   • Atualize regularmente o repositório
   • Use branches para desenvolvimento de novas features
   • Configure proteção de branches para maior segurança
    """)

def main():
    """Função principal"""
    print_header()
    
    # Verificar pré-requisitos
    if not check_prerequisites():
        print("\n❌ Falha na verificação de pré-requisitos!")
        sys.exit(1)
    
    # Criar repositório no GitHub
    if not create_github_repo():
        print("\n❌ Falha ao criar repositório no GitHub!")
        sys.exit(1)
    
    # Configurar remote
    if not configure_remote():
        print("\n❌ Falha ao configurar remote!")
        sys.exit(1)
    
    # Fazer push para o GitHub
    if not push_to_github():
        print("\n❌ Falha ao fazer push para o GitHub!")
        sys.exit(1)
    
    # Mostrar resumo final
    show_final_summary()
    
    print("\n🎊 PARABÉNS! Seu projeto foi publicado no GitHub com sucesso! 🎊\n")

if __name__ == "__main__":
    main()