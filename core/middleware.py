import logging

logger = logging.getLogger(__name__)

class CSRFDebugMiddleware:
    """Middleware para debug de problemas CSRF na SquareCloud"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log informações da requisição para debug
        if request.method == 'POST' and '/admin/' in request.path:
            logger.info(f"POST request to {request.path}")
            logger.info(f"Host: {request.get_host()}")
            logger.info(f"Origin: {request.META.get('HTTP_ORIGIN', 'No Origin')}")
            logger.info(f"Referer: {request.META.get('HTTP_REFERER', 'No Referer')}")
            logger.info(f"X-Forwarded-Proto: {request.META.get('HTTP_X_FORWARDED_PROTO', 'No Proto')}")

        response = self.get_response(request)
        return response