from django.urls import path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .views import (
    user_register, user_login, user_dashboard, create_event, user_logout,
    events_list, event_detail, register_for_event, unregister_from_event, my_registrations
)

@login_required
def user_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')
    
    return render(request, 'users/profile.html')

urlpatterns = [
    path('register/', user_register, name='user_register'),
    path('login/', user_login, name='user_login'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('create-event/', create_event, name='create_event'),
    path('logout/', user_logout, name='user_logout'),
    path('profile/', user_profile, name='user_profile'),
    path('events/', events_list, name='events_list'),
    path('events/<int:event_id>/', event_detail, name='event_detail'),
    path('events/<int:event_id>/register/', register_for_event, name='register_for_event'),
    path('events/<int:event_id>/unregister/', unregister_from_event, name='unregister_from_event'),
    path('my-registrations/', my_registrations, name='my_registrations'),
]