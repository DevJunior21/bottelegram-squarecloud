from django.core.management.base import BaseCommand
from django.conf import settings
import requests

class Command(BaseCommand):
    help = 'Configura o webhook do Telegram'
    
    def handle(self, *args, **options):
        if not settings.BOT_TOKEN:
            self.stdout.write(
                self.style.ERROR('BOT_TOKEN não configurado!')
            )
            return
            
        if not settings.WEBHOOK_URL:
            self.stdout.write(
                self.style.ERROR('WEBHOOK_URL não configurado!')
            )
            return
            
        # Configurar webhook
        url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/setWebhook"
        data = {
            'url': settings.WEBHOOK_URL
        }
        
        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    self.stdout.write(
                        self.style.SUCCESS('Webhook configurado com sucesso!')
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(f'Erro ao configurar webhook: {result.get("description")}')
                    )
            else:
                self.stdout.write(
                    self.style.ERROR(f'Erro HTTP: {response.status_code}')
                )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Erro ao configurar webhook: {e}')
            )