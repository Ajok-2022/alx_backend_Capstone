from django.contrib import admin
from .models import Event, EventRegistration

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'date_time', 'location', 'capacity', 'available_spots']
    list_filter = ['date_time', 'organizer']
    search_fields = ['title', 'location', 'organizer__username']
    readonly_fields = ['created_date', 'available_spots']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'registered_at']
    list_filter = ['registered_at', 'event']
    search_fields = ['user__username', 'event__title']