from django.urls import path
from .api_views import register, login_api, logout_api, profile

urlpatterns = [
    path('register/', register, name='api_register'),
    path('login/', login_api, name='api_login'),
    path('logout/', logout_api, name='api_logout'),
    path('profile/', profile, name='api_profile'),
]