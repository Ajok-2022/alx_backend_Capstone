from rest_framework import serializers
from django.utils import timezone
from .models import Event, EventRegistration

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField(read_only=True)
    available_spots = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date_time', 'location', 
                 'organizer', 'capacity', 'created_date', 'available_spots', 
                 'is_full', 'is_upcoming']
        read_only_fields = ['id', 'organizer', 'created_date']
    
    def validate_date_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Event date must be in the future.")
        return value
    
    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Capacity must be greater than 0.")
        return value

class EventRegistrationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    
    class Meta:
        model = EventRegistration
        fields = ['id', 'event', 'event_title', 'registered_at']
        read_only_fields = ['id', 'registered_at']