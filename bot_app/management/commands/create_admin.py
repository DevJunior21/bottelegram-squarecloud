from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Cria um superusuário padrão se não existir'
    
    def handle(self, *args, **options):
        User = get_user_model()
        
        # Verificar se o superusuário já existe
        if not User.objects.filter(username='admin').exists():
            # Criar superusuário
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='Suzuya2109@bot/'
            )
            self.stdout.write(
                self.style.SUCCESS('Superusuário "admin" criado com sucesso!')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Superusuário "admin" já existe.')
            )