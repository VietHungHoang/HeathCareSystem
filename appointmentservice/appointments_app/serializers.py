from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id',
            'patient_id',
            'doctor_id',
            'appointment_time',
            'duration_minutes',
            'status',
            'reason_for_visit',
            'doctor_notes',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')

class AppointmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['status', 'doctor_notes']