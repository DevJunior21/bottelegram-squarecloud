from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Reseta a senha do admin ou cria se não existir'

    def handle(self, *args, **options):
        User = get_user_model()

        try:
            # Tentar encontrar o usuário admin
            admin_user = User.objects.get(username='admin')
            # Resetar senha
            admin_user.set_password('Suzuya2109@bot/')
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS('Senha do admin resetada com sucesso!')
            )
        except User.DoesNotExist:
            # Criar novo admin
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='Suzuya2109@bot/'
            )
            self.stdout.write(
                self.style.SUCCESS('Superusuário "admin" criado com sucesso!')
            )

        # Mostrar credenciais
        self.stdout.write(
            self.style.WARNING('=== CREDENCIAIS DO ADMIN ===')
        )
        self.stdout.write(f'Usuário: admin')
        self.stdout.write(f'Senha: Suzuya2109@bot/')
        self.stdout.write(
            self.style.WARNING('=============================')
        )