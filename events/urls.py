from django.urls import path
from .views import (
    EventListCreateView, EventDetailView, UpcomingEventsView, 
    MyEventsView, register_for_event, unregister_from_event
)

urlpatterns = [
    path('', EventListCreateView.as_view(), name='event-list-create'),
    path('<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('upcoming/', UpcomingEventsView.as_view(), name='upcoming-events'),
    path('my-events/', MyEventsView.as_view(), name='my-events'),
    path('<int:event_id>/register/', register_for_event, name='register-event'),
    path('<int:event_id>/unregister/', unregister_from_event, name='unregister-event'),
]