from rest_framework import serializers
from .models import CalendarEvent  # Assuming CalendarEvent model is defined in models.py


class UserSignupStatsSerializer(serializers.Serializer):
    date = serializers.DateField()
    count = serializers.IntegerField()


class CalendarEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarEvent
        fields = ['id', 'title', 'description', 'date', 'time']
        read_only_fields = ['id']
