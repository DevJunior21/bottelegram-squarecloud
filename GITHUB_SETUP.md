# Configuração do Repositório GitHub

Este documento fornece instruções passo a passo para criar um repositório no GitHub e fazer upload do projeto BotTelegram.

## Passo 1: Criar um Token de Acesso Pessoal no GitHub

1. Acesse [GitHub](https://github.com) e faça login
2. Clique no seu perfil no canto superior direito e selecione "Settings"
3. No menu lateral esquerdo, role para baixo e clique em "Developer settings"
4. Clique em "Personal access tokens" e depois em "Tokens (classic)"
5. Clique no botão "Generate new token" e selecione "Generate new token (classic)"
6. Dê um nome descritivo ao token (ex: "BotTelegram SquareCloud")
7. Selecione as seguintes permissões:
   - `repo` (todas as permissões relacionadas a repositórios)
   - `admin:org` (se for criar repositórios organizacionais)
   - `gist` (opcional)
8. Clique em "Generate token"
9. **Importante**: Copie o token gerado e guarde-o em local seguro (você não poderá vê-lo novamente)

## Passo 2: Configurar o Token como Variável de Ambiente

No terminal, defina o token como variável de ambiente:

```bash
export GITHUB_TOKEN=seu_token_aqui
```

Substitua `seu_token_aqui` pelo token que você copiou no passo anterior.

## Passo 3: Executar o Script de Criação do Repositório

Agora execute o script que criamos:

```bash
cd /root/bottelegram_squarecloud
chmod +x create_github_repo.sh
./create_github_repo.sh
```

## Passo 4: Verificar o Repositório

Após a execução bem-sucedida do script:

1. Acesse https://github.com/seu-usuario/bottelegram-squarecloud
2. Verifique se os arquivos foram enviados corretamente
3. Confirme se o README.md está sendo exibido na página inicial

## Solução de Problemas

### Se o script falhar com erro de autenticação:

1. Verifique se o token foi configurado corretamente:
   ```bash
   echo $GITHUB_TOKEN
   ```
   
2. Certifique-se de que o token tem as permissões necessárias

3. Se necessário, gere um novo token e tente novamente

### Se o repositório já existir:

1. Você pode usar o mesmo repositório existente
2. Ou deletar o repositório existente e criar um novo
3. Ou modificar o script para usar um nome diferente

### Se ocorrer erro ao fazer push:

1. Verifique se há commits no repositório local:
   ```bash
   cd /root/bottelegram_squarecloud
   git log --oneline
   ```

2. Verifique o status do remote:
   ```bash
   git remote -v
   ```

3. Tente fazer push manualmente:
   ```bash
   git push -u origin main
   ```

## Comandos Úteis Git

### Verificar status do repositório:
```bash
git status
```

### Ver histórico de commits:
```bash
git log --oneline --graph
```

### Ver remotes configurados:
```bash
git remote -v
```

### Adicionar novos arquivos e fazer commit:
```bash
git add .
git commit -m "Descrição das mudanças"
git push
```

## Próximos Passos

Após configurar o repositório no GitHub:

1. Configure webhooks para integração contínua (se necessário)
2. Adicione colaboradores ao repositório (se for trabalhar em equipe)
3. Configure proteção de branches para maior segurança
4. Adicione descrição, tópicos e website (opcional) nas configurações do repositório

## Referências

- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [Git Documentation](https://git-scm.com/doc)