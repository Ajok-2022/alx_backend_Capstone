from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Event, EventRegistration
from .serializers import EventSerializer, EventRegistrationSerializer

class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Event.objects.all()
        title = self.request.query_params.get('title')
        location = self.request.query_params.get('location')
        if title:
            queryset = queryset.filter(title__icontains=title)
        if location:
            queryset = queryset.filter(location__icontains=location)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Event.objects.all()
    
    def get_object(self):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if event.organizer != self.request.user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied("You can only modify events you created.")
        return event

class UpcomingEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Event.objects.filter(date_time__gt=timezone.now())
        title = self.request.query_params.get('title')
        location = self.request.query_params.get('location')
        if title:
            queryset = queryset.filter(title__icontains=title)
        if location:
            queryset = queryset.filter(location__icontains=location)
        return queryset

class MyEventsView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if event.organizer == request.user:
        return Response(
            {"error": "You cannot register for your own event"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if event.is_full:
        return Response(
            {"error": "Event is at full capacity"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not event.is_upcoming:
        return Response(
            {"error": "Cannot register for past events"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    registration, created = EventRegistration.objects.get_or_create(
        user=request.user, 
        event=event
    )
    
    if not created:
        return Response(
            {"error": "Already registered for this event"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    serializer = EventRegistrationSerializer(registration)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unregister_from_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    try:
        registration = EventRegistration.objects.get(user=request.user, event=event)
        registration.delete()
        return Response(
            {"message": "Successfully unregistered from event"}, 
            status=status.HTTP_200_OK
        )
    except EventRegistration.DoesNotExist:
        return Response(
            {"error": "Not registered for this event"}, 
            status=status.HTTP_400_BAD_REQUEST
        )