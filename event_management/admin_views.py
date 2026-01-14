from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from events.models import Event, EventRegistration
from events.serializers import EventSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

def is_staff(user):
    return user.is_staff

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('/admin-panel/dashboard/')
        messages.error(request, 'Invalid credentials or not staff user')
    return render(request, 'admin/login.html')

@login_required
@user_passes_test(is_staff)
def admin_dashboard(request):
    events_count = Event.objects.count()
    users_count = User.objects.count()
    registrations_count = EventRegistration.objects.count()
    recent_events = Event.objects.order_by('-created_date')[:5]
    
    context = {
        'events_count': events_count,
        'users_count': users_count,
        'registrations_count': registrations_count,
        'recent_events': recent_events,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_staff)
def admin_events(request):
    events = Event.objects.all().order_by('-created_date')
    return render(request, 'admin/events.html', {'events': events})

@login_required
@user_passes_test(is_staff)
def admin_users(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin/users.html', {'users': users})

@login_required
@user_passes_test(is_staff)
def admin_registrations(request):
    registrations = EventRegistration.objects.all().order_by('-registered_at')
    return render(request, 'admin/registrations.html', {'registrations': registrations})

def admin_logout(request):
    logout(request)
    return redirect('/admin-panel/')