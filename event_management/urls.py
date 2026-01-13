from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import api_home

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
    path('', api_home, name='api-home'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),
    path('api/events/', include('events.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]