import uuid
from django.db import models

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient_id = models.UUIDField()
    doctor_id = models.UUIDField()
    appointment_time = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='SCHEDULED')
    reason_for_visit = models.TextField(null=True, blank=True)
    doctor_notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appointment {self.id} on {self.appointment_time.date()}"

    class Meta:
        db_table = 'appointments'
        ordering = ['-appointment_time']