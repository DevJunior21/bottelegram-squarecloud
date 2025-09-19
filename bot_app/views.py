from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from django.contrib.auth import get_user_model
import json
import logging

# Configurar logger
logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def telegram_webhook(request):
    """Webhook do Telegram"""
    try:
        # Parse do JSON recebido
        data = json.loads(request.body)
        logger.info(f"Recebido update do Telegram: {data}")

        # Processar a atualização do Telegram
        # Implementar lógica específica do bot aqui

        return JsonResponse({'status': 'ok'})
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        return JsonResponse({'error': str(e)}, status=500)

def index(request):
    """Página inicial do bot"""
    return JsonResponse({
        'status': 'online',
        'message': 'BotTelegram está rodando',
        'platform': 'SquareCloud',
        'setup_url': '/setup-admin/'
    })

def setup_admin(request):
    """Setup inicial - criar admin sem terminal"""
    User = get_user_model()

    try:
        # Verificar se admin já existe
        if User.objects.filter(username='admin').exists():
            admin_user = User.objects.get(username='admin')
            # Resetar senha para garantir que funciona
            admin_user.set_password('Suzuya2109@bot/')
            admin_user.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Admin já existe - senha resetada',
                'username': 'admin',
                'password': 'Suzuya2109@bot/',
                'admin_url': '/admin/',
                'action': 'password_reset'
            })
        else:
            # Criar novo admin
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='Suzuya2109@bot/'
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Admin criado com sucesso!',
                'username': 'admin',
                'password': 'Suzuya2109@bot/',
                'admin_url': '/admin/',
                'action': 'created'
            })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Erro ao criar admin: {str(e)}'
        }, status=500)