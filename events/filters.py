import django_filters
from django.utils import timezone
from .models import Event

class EventFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    date_from = django_filters.DateTimeFilter(field_name='date_time', lookup_expr='gte')
    date_to = django_filters.DateTimeFilter(field_name='date_time', lookup_expr='lte')
    upcoming = django_filters.BooleanFilter(method='filter_upcoming')
    
    class Meta:
        model = Event
        fields = ['title', 'location', 'date_from', 'date_to', 'upcoming']
    
    def filter_upcoming(self, queryset, name, value):
        if value:
            return queryset.filter(date_time__gt=timezone.now())
        return queryset