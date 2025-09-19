import os
import requests
import uuid
from datetime import datetime

PUSHINPAY_API_URL = 'https://api.pushinpay.com.br/api'
PUSHINPAY_API_TOKEN = os.getenv('PUSHINPAY_API_TOKEN')

HEADERS = {
    'Authorization': f'Bearer {PUSHINPAY_API_TOKEN}',
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

def criar_cobranca_pix(value_centavos, webhook_url, split_rules=None):
    # Se não há token configurado, usar modo de teste
    if not PUSHINPAY_API_TOKEN:
        return criar_cobranca_pix_teste(value_centavos, webhook_url)
    
    payload = {
        'value': value_centavos,
        'webhook_url': webhook_url,
    }
    if split_rules:
        payload['split_rules'] = split_rules
    response = requests.post(f'{PUSHINPAY_API_URL}/pix/cashIn', json=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def criar_cobranca_pix_teste(value_centavos, webhook_url):
    """
    Função de teste que simula a criação de PIX quando as variáveis não estão configuradas.
    """
    transaction_id = str(uuid.uuid4())
    valor_reais = value_centavos / 100
    
    return {
        'id': transaction_id,
        'qr_code': f'PIX de teste - R$ {valor_reais:.2f}\nTransaction ID: {transaction_id}\n\n⚠️ MODO DE TESTE - Configure PUSHINPAY_API_TOKEN para usar PIX real',
        'qr_code_base64': None,  # Não gerar QR code em teste
        'status': 'PENDING',
        'value': value_centavos,
        'created_at': datetime.now().isoformat()
    }

def consultar_transacao(transaction_id):
    # Se não há token configurado, retornar status simulado
    if not PUSHINPAY_API_TOKEN:
        return {
            'id': transaction_id,
            'status': 'PENDING',
            'message': 'Modo de teste - Configure PUSHINPAY_API_TOKEN para consulta real'
        }
    
    response = requests.get(f'{PUSHINPAY_API_URL}/transactions/{transaction_id}', headers=HEADERS)
    response.raise_for_status()
    return response.json()
