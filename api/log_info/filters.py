from django_filters.rest_framework import FilterSet

from apps.alert.models import NotificationPrivateMessage


class NotificationFilterSet(FilterSet):
    class Meta:
        model = NotificationPrivateMessage
        fields = ("client", "active_until", "is_active")
