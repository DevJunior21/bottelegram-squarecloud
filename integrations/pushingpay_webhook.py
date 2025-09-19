import os
import hmac
import hashlib
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings

logger = logging.getLogger(__name__)

def verificar_assinatura_webhook(payload, signature, secret):
    """
    Verifica a assinatura do webhook da PushingPay
    """
    if not secret:
        logger.warning("Webhook secret não configurado")
        return False

    # Calcular a assinatura esperada usando SHA256
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    # Comparar as assinaturas de forma segura
    return hmac.compare_digest(signature, expected_signature)

def processar_webhook_pushinpay(data):
    """
    Processa o webhook da PushingPay
    """
    try:
        # Importar aqui para evitar dependência circular
        from bot_app.models import Pagamento

        transaction_id = data.get('transaction_id') or data.get('id')
        status = data.get('status', '').upper()

        if not transaction_id:
            logger.error("Transaction ID não encontrado no webhook")
            return False

        try:
            pagamento = Pagamento.objects.get(pushinpay_transaction_id=transaction_id)

            # Mapear status da PushinPay para nosso sistema
            if status in ['PAID', 'CONFIRMED', 'APPROVED']:
                pagamento.status = 'pago'
                # Ativar assinatura
                if pagamento.assinatura:
                    pagamento.assinatura.status = 'ativa'
                    pagamento.assinatura.save()
                    logger.info(f"Assinatura {pagamento.assinatura.id} ativada via webhook")

            elif status in ['CANCELLED', 'EXPIRED', 'FAILED']:
                pagamento.status = 'cancelado'
            elif status in ['PENDING', 'WAITING']:
                pagamento.status = 'pendente'

            pagamento.save()
            logger.info(f"Pagamento {pagamento.id} atualizado para status: {pagamento.status}")
            return True

        except Pagamento.DoesNotExist:
            logger.error(f"Pagamento com transaction_id {transaction_id} não encontrado")
            return False

    except Exception as e:
        logger.error(f"Erro ao processar webhook PushinPay: {e}")
        return False

@csrf_exempt
@require_http_methods(["POST"])
def pushinpay_webhook_handler(request):
    """
    Handler principal do webhook da PushingPay
    """
    try:
        # Obter o secret do webhook das configurações
        webhook_secret = getattr(settings, 'PUSHINGPAY_WEBHOOK_SECRET', '')

        # Obter assinatura do header
        signature = request.META.get('HTTP_X_SIGNATURE', '')

        # Verificar assinatura se o secret estiver configurado
        if webhook_secret and signature:
            if not verificar_assinatura_webhook(request.body, signature, webhook_secret):
                logger.warning("Assinatura do webhook PushinPay inválida")
                return JsonResponse({'error': 'Invalid signature'}, status=401)
        elif webhook_secret:
            logger.warning("Webhook secret configurado mas assinatura não encontrada")
            return JsonResponse({'error': 'Missing signature'}, status=401)
        else:
            logger.warning("Webhook PushinPay recebido sem verificação de assinatura")

        # Parse do JSON
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            logger.error("Erro ao decodificar JSON do webhook PushinPay")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        logger.info(f"Webhook PushinPay recebido: {data}")

        # Processar webhook
        if processar_webhook_pushinpay(data):
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'error': 'Processing failed'}, status=400)

    except Exception as e:
        logger.error(f"Erro no handler do webhook PushinPay: {e}")
        return JsonResponse({'error': 'Internal server error'}, status=500)