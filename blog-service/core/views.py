import json
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from rest_framework.decorators import api_view


@api_view(['GET'])
def health_check(request):
    """
    Healthcheck endpoint que verifica DB y Redis
    """
    health_status = {
        'status': 'healthy',
        'service': 'blog-service',
        'version': '1.0.0',
        'checks': {}
    }
    
    # Check Database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        health_status['checks']['database'] = 'ok'
    except Exception as e:
        health_status['checks']['database'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    # Check Redis
    try:
        cache.set('health_check', 'ok', 10)
        cache_result = cache.get('health_check')
        if cache_result == 'ok':
            health_status['checks']['redis'] = 'ok'
        else:
            health_status['checks']['redis'] = 'error: cache test failed'
            health_status['status'] = 'unhealthy'
    except Exception as e:
        health_status['checks']['redis'] = f'error: {str(e)}'
        health_status['status'] = 'unhealthy'
    
    status_code = 200 if health_status['status'] == 'healthy' else 503
    return JsonResponse(health_status, status=status_code)