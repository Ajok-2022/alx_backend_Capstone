from django.urls import path, include, re_path
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import api_home
from .admin_views import (
    admin_login, admin_dashboard, admin_events, 
    admin_users, admin_registrations, admin_logout
)
from users.views import (
    user_register, user_login, user_dashboard, create_event, user_logout,
    events_list, event_detail, register_for_event, unregister_from_event, my_registrations, user_profile, delete_event
)

def redirect_to_admin(request):
    return redirect('/admin-panel/')

def redirect_login(request):
    next_url = request.GET.get('next', '')
    if next_url:
        return HttpResponseRedirect(f'/users/login/?next={next_url}')
    return HttpResponseRedirect('/users/login/')

def redirect_register(request):
    return HttpResponseRedirect('/users/register/')

def redirect_logout(request):
    return HttpResponseRedirect('/users/logout/')

def redirect_dashboard(request):
    return HttpResponseRedirect('/users/dashboard/')

schema_view = get_schema_view(
   openapi.Info(
      title="Event Management API",
      default_version='v1',
      description="A comprehensive REST API for managing events with authentication and registration",
      contact=openapi.Contact(email="ajokkuechajokdeng@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', redirect, {'url': '/events/'}, name='home'),
    path('home/', api_home, name='api-home'),
    
    # Legacy redirects
    path('login/', redirect_login, name='legacy_login'),
    path('register/', redirect_register, name='legacy_register'),
    path('logout/', redirect_logout, name='legacy_logout'),
    path('dashboard/', redirect_dashboard, name='legacy_dashboard'),
    
    # User Authentication
    path('users/register/', user_register, name='user_register'),
    path('users/login/', user_login, name='user_login'),
    path('users/logout/', user_logout, name='user_logout'),

    
    # User Pages
    path('users/dashboard/', user_dashboard, name='user_dashboard'),
    path('users/create-event/', create_event, name='create_event'),
    path('users/my-registrations/', my_registrations, name='my_registrations'),
    path('users/profile/', user_profile, name='user_profile'),
    
    # Events
    path('events/', events_list, name='events_list'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),
    path('events/<int:event_id>/register/', register_for_event, name='register_for_event'),
    path('events/<int:event_id>/unregister/', unregister_from_event, name='unregister_from_event'),
    path('events/<int:event_id>/delete/', delete_event, name='delete_event'),
    
    # Admin Panel
    path('admin/', redirect_to_admin),
    path('admin-panel/', admin_login, name='admin_login'),
    path('admin-panel/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('admin-panel/events/', admin_events, name='admin_events'),
    path('admin-panel/users/', admin_users, name='admin_users'),
    path('admin-panel/registrations/', admin_registrations, name='admin_registrations'),
    path('admin-panel/logout/', admin_logout, name='admin_logout'),
    
    # API
    path('api/users/', include('users.api_urls')),
    path('api/events/', include('events.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]