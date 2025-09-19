from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
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
        'platform': 'SquareCloud'
    })