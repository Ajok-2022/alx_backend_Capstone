from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_time = models.DateTimeField()
    location = models.CharField(max_length=300)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    capacity = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    attendees = models.ManyToManyField(User, through='EventRegistration', related_name='attending_events')
    
    class Meta:
        ordering = ['date_time']
    
    def __str__(self):
        return self.title
    
    @property
    def is_upcoming(self):
        return self.date_time > timezone.now()
    
    @property
    def available_spots(self):
        return self.capacity - self.attendees.count()
    
    @property
    def is_full(self):
        return self.attendees.count() >= self.capacity

class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'event')
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"