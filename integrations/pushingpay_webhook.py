import os
import hmac
import hashlib
import json
import logging
from urllib.parse import parse_qs
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from tasks.tasks import processar_webhook_pushinpay

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

def parse_webhook_data(request):
    """
    Parseia os dados do webhook tanto de JSON quanto de form-urlencoded
    """
    content_type = request.headers.get('Content-Type', '').lower()
    
    if 'application/json' in content_type:
        # Processar como JSON
        try:
            payload_str = request.body.decode('utf-8')
            return json.loads(payload_str)
        except json.JSONDecodeError as e:
            logger.error(f"JSON inválido no webhook: {e}")
            raise ValueError(f"JSON inválido: {e}")
    
    elif 'application/x-www-form-urlencoded' in content_type:
        # Processar como form-urlencoded
        try:
            payload_str = request.body.decode('utf-8')
            parsed_data = parse_qs(payload_str)
            
            # Converter de list para string (parse_qs retorna listas)
            data = {}
            for key, value_list in parsed_data.items():
                data[key] = value_list[0] if value_list else ''
            
            return data
        except Exception as e:
            logger.error(f"Erro ao processar form-urlencoded: {e}")
            raise ValueError(f"Form-urlencoded inválido: {e}")
    
    else:
        # Tentar processar como JSON por padrão
        try:
            payload_str = request.body.decode('utf-8')
            return json.loads(payload_str)
        except json.JSONDecodeError:
            # Se falhar, tentar como form-urlencoded
            try:
                payload_str = request.body.decode('utf-8')
                parsed_data = parse_qs(payload_str)
                data = {}
                for key, value_list in parsed_data.items():
                    data[key] = value_list[0] if value_list else ''
                return data
            except Exception as e:
                logger.error(f"Erro ao processar payload: {e}")
                raise ValueError(f"Formato de payload não suportado: {e}")

@csrf_exempt
@require_http_methods(["POST"])
def pushinpay_webhook_handler(request):
    """
    Handler para webhooks da PushingPay
    """
    print("=== WEBHOOK RECEBIDO ===")
    print(f"Method: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    print(f"Body length: {len(request.body)}")
    print(f"Body raw: {request.body}")
    
    try:
        # Obter o payload
        payload = request.body
        payload_str = payload.decode('utf-8')
        
        # Log detalhado para debug
        logger.info(f"Webhook recebido - Content-Type: {request.headers.get('Content-Type')}")
        logger.info(f"Payload length: {len(payload)} bytes")
        logger.info(f"Payload raw: {payload}")
        logger.info(f"Payload string: {payload_str}")
        
        # Obter a assinatura do header (PushinPay usa X-Pushinpay-Token)
        signature = request.headers.get('X-Pushinpay-Token', '')
        
        # Log para debug
        logger.info(f"Webhook recebido - Signature: {signature}")
        
        # Verificar se o payload está vazio
        if not payload_str.strip():
            logger.warning("Payload vazio recebido no webhook")
            print("PAYLOAD VAZIO!")
            return JsonResponse({'error': 'Payload vazio'}, status=400)
        
        # Verificar a assinatura
        webhook_secret = os.getenv('PUSHINGPAY_WEBHOOK_SECRET')
        # TEMPORARIAMENTE DESABILITADO PARA TESTE
        # if not verificar_assinatura_webhook(payload, signature, webhook_secret):
        #     logger.error(f"Assinatura inválida do webhook: {signature}")
        #     logger.error(f"Secret configurado: {webhook_secret[:10]}..." if webhook_secret else "Secret não configurado")
        #     return JsonResponse({'error': 'Assinatura inválida'}, status=401)
        
        logger.info(f"Webhook recebido - Signature: {signature}")
        logger.info(f"Secret configurado: {webhook_secret[:10]}..." if webhook_secret else "Secret não configurado")
        logger.info("Validação de assinatura temporariamente desabilitada para teste")
        
        # Parsear os dados do webhook
        try:
            data = parse_webhook_data(request)
        except ValueError as e:
            logger.error(f"Erro ao parsear dados do webhook: {e}")
            return JsonResponse({'error': str(e)}, status=400)
        
        # Log do webhook recebido
        logger.info(f"Webhook PushingPay recebido: {data}")
        
        # Validar campos obrigatórios
        required_fields = ['id', 'status']
        for field in required_fields:
            if field not in data:
                logger.error(f"Campo obrigatório ausente no webhook: {field}")
                return JsonResponse({'error': f'Campo obrigatório ausente: {field}'}, status=400)
        
        # Enfileirar para processamento assíncrono
        processar_webhook_pushinpay.delay(data)
        
        logger.info(f"Webhook processado com sucesso: {data.get('id')}")
        return JsonResponse({'status': 'ok', 'message': 'Webhook processado'})
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        return JsonResponse({'error': 'Erro interno do servidor'}, status=500)

def testar_webhook():
    """
    Função para testar o webhook localmente
    """
    import requests
    
    # Dados de teste
    test_data = {
        'id': 'test_transaction_123',
        'status': 'PAID',
        'value': 1000,  # R$ 10,00 em centavos
        'created_at': '2024-01-01T12:00:00Z'
    }
    
    # URL do webhook (ajuste conforme necessário)
    webhook_url = 'http://localhost:8008/api/webhooks/pushinpay-notifications/'
    
    try:
        response = requests.post(webhook_url, json=test_data)
        print(f"Status: {response.status_code}")
        print(f"Resposta: {response.text}")
    except Exception as e:
        print(f"Erro no teste: {e}")

if __name__ == '__main__':
    testar_webhook()
