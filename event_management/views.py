from django.http import JsonResponse
from django.shortcuts import render

def api_home(request):
    """API Home page with documentation"""
    if request.content_type == 'application/json' or 'application/json' in request.META.get('HTTP_ACCEPT', ''):
        return JsonResponse({
            'message': 'Welcome to Event Management API',
            'version': '1.0.0',
            'endpoints': {
                'authentication': {
                    'register': '/api/auth/register/',
                    'login': '/api/auth/login/',
                    'profile': '/api/auth/profile/'
                },
                'events': {
                    'list_create': '/api/events/',
                    'detail': '/api/events/{id}/',
                    'upcoming': '/api/events/upcoming/',
                    'my_events': '/api/events/my-events/',
                    'register': '/api/events/{id}/register/',
                    'unregister': '/api/events/{id}/unregister/'
                },
                'admin': '/admin/',
                'docs': {
                    'swagger': '/swagger/',
                    'redoc': '/redoc/'
                }
            }
        })
    
    return render(request, 'home.html')