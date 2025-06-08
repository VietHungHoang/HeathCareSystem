from rest_framework import serializers
from .models import Doctor, WorkSchedule

class WorkScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSchedule
        fields = ['id', 'day_of_week', 'start_time', 'end_time', 'shift_name']


class DoctorSerializer(serializers.ModelSerializer):
    schedules = WorkScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id',
            'user_id',
            'specialty',
            'degrees',
            'experience_years',
            'bio',
            'schedules',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'schedules', 'created_at', 'updated_at']


class AvailabilityCheckSerializer(serializers.Serializer):
    datetime = serializers.DateTimeField()