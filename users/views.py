from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from events.models import Event, EventRegistration

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully! Please login.')
            return redirect('/login/')
    
    return render(request, 'users/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', '/dashboard/')
            return redirect(next_url)
        messages.error(request, 'Invalid username or password')
    
    return render(request, 'users/login.html')

@login_required
def user_dashboard(request):
    my_events = Event.objects.filter(organizer=request.user)
    registered_events = Event.objects.filter(attendees=request.user)
    upcoming_events = Event.objects.filter(date_time__gt=timezone.now())[:5]
    
    context = {
        'my_events': my_events,
        'registered_events': registered_events,
        'upcoming_events': upcoming_events,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def create_event(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        date_time = request.POST['date_time']
        location = request.POST['location']
        capacity = request.POST['capacity']
        
        Event.objects.create(
            title=title,
            description=description,
            date_time=date_time,
            location=location,
            capacity=capacity,
            organizer=request.user
        )
        messages.success(request, 'Event created successfully!')
        return redirect('user_dashboard')
    
    return render(request, 'users/create_event.html')

def events_list(request):
    search = request.GET.get('search', '')
    location_filter = request.GET.get('location', '')
    
    events = Event.objects.filter(date_time__gt=timezone.now()).order_by('date_time')
    
    if search:
        events = events.filter(title__icontains=search)
    if location_filter:
        events = events.filter(location__icontains=location_filter)
    
    locations = Event.objects.values_list('location', flat=True).distinct()
    
    context = {
        'events': events,
        'locations': locations,
        'search': search,
        'location_filter': location_filter,
    }
    return render(request, 'users/events_list.html', context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_registered = False
    if request.user.is_authenticated:
        is_registered = EventRegistration.objects.filter(user=request.user, event=event).exists()
    
    context = {
        'event': event,
        'is_registered': is_registered,
    }
    return render(request, 'users/event_detail.html', context)

@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if event.organizer == request.user:
        messages.error(request, 'You cannot register for your own event')
    elif event.is_full:
        messages.error(request, 'Event is at full capacity')
    elif not event.is_upcoming:
        messages.error(request, 'Cannot register for past events')
    elif EventRegistration.objects.filter(user=request.user, event=event).exists():
        messages.error(request, 'Already registered for this event')
    else:
        EventRegistration.objects.create(user=request.user, event=event)
        messages.success(request, f'Successfully registered for {event.title}!')
    
    return redirect('event_detail', event_id=event_id)

@login_required
def unregister_from_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    try:
        registration = EventRegistration.objects.get(user=request.user, event=event)
        registration.delete()
        messages.success(request, f'Successfully unregistered from {event.title}')
    except EventRegistration.DoesNotExist:
        messages.error(request, 'Not registered for this event')
    
    return redirect('event_detail', event_id=event_id)

@login_required
def my_registrations(request):
    registrations = EventRegistration.objects.filter(user=request.user).order_by('-registered_at')
    return render(request, 'users/my_registrations.html', {'registrations': registrations})

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

@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, organizer=request.user)
    
    if request.method == 'POST':
        event_title = event.title
        event.delete()
        messages.success(request, f'Event "{event_title}" has been deleted successfully.')
        return redirect('user_dashboard')
    
    return redirect('event_detail', event_id=event_id)

def user_logout(request):
    logout(request)
    return redirect('/events/')