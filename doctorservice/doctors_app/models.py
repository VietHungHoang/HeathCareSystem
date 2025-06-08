import uuid
from django.db import models

class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(unique=True)
    specialty = models.CharField(max_length=255)
    degrees = models.TextField(null=True, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. (user_id: {self.user_id})"

    class Meta:
        db_table = 'doctors'

class WorkSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField()  # 0=Monday, 1=Tuesday, ..., 6=Sunday
    start_time = models.TimeField()
    end_time = models.TimeField()
    shift_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.doctor} - {self.get_day_of_week_display()} ({self.start_time} - {self.end_time})"

    class Meta:
        db_table = 'work_schedules'
        unique_together = ('doctor', 'day_of_week', 'start_time', 'end_time')