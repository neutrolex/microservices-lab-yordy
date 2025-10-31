import json
import time
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('blog_service')


class LoggingMiddleware(MiddlewareMixin):
    """Middleware para logging estructurado JSON por request"""
    
    def process_request(self, request):
        request.start_time = time.time()
        
    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            
            log_data = {
                'method': request.method,
                'path': request.path,
                'status_code': response.status_code,
                'duration_ms': round(duration * 1000, 2),
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'remote_addr': self.get_client_ip(request),
            }
            
            logger.info(json.dumps(log_data))
            
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class AuthHeaderMiddleware(MiddlewareMixin):
    """Middleware que lee Authorization header (preparación para mañana)"""
    
    def process_request(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            logger.info(f"Authorization header detected: Bearer {token[:20]}...")
            # TODO: Mañana validar token con Auth Service
            request.jwt_token = token
        return None