# BotTelegram SquareCloud

Bot Telegram otimizado para deploy na plataforma SquareCloud.

## Descrição

Este projeto é uma versão otimizada do BotTelegram para ser executado na plataforma SquareCloud. Ele inclui todas as configurações necessárias para deploy simplificado na plataforma.

## Estrutura do Projeto

- `core/` - Configurações principais do Django
- `bot/` - Código do bot Telegram
- `tasks/` - Tarefas assíncronas
- `integrations/` - Integrações com APIs externas
- `promocoes/` - Sistema de promoções
- `carrossel/` - Sistema de carrossel de ofertas
- `welcome/` - Sistema de boas-vindas
- `static/` - Arquivos estáticos
- `media/` - Arquivos de mídia
- `logs/` - Arquivos de log

## Requisitos

- Python 3.10+
- Django 4.2.11
- python-telegram-bot 20.0
- PostgreSQL (para ambiente de produção)
- Redis (para ambiente de produção)

## Configuração

1. Crie um arquivo `.env` com as variáveis de ambiente necessárias:
   ```
   DEBUG=True
   DJANGO_SECRET_KEY=sua_chave_secreta_aqui
   TELEGRAM_BOT_TOKEN=seu_token_do_bot_telegram_aqui
   DATABASE_URL=postgresql://usuario:senha@host:porta/banco
   REDIS_URL=redis://host:porta
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

4. Colete os arquivos estáticos:
   ```bash
   python manage.py collectstatic --noinput
   ```

5. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

## Deploy na SquareCloud

1. Crie uma conta na [SquareCloud](https://squarecloud.app)
2. Crie um novo aplicativo
3. Faça upload dos arquivos do projeto
4. Configure as variáveis de ambiente na plataforma
5. Inicie o aplicativo

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.