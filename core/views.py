from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    """Página inicial do bot"""
    return JsonResponse({
        'status': 'online',
        'message': 'BotTelegram está rodando',
        'platform': 'SquareCloud'
    })

@csrf_exempt
def telegram_webhook(request):
    """Webhook do Telegram"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Processar a atualização do Telegram
            # Implementar lógica específica do bot aqui
            
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)