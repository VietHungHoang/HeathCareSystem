# doctors_app/views.py

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Doctor, WorkSchedule
from .serializers import DoctorSerializer, WorkScheduleSerializer, AvailabilityCheckSerializer

# --- Doctor Views ---

# /api/doctors/
class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

# /api/doctors/{doctor_id}/
class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    lookup_field = 'id'

# /api/doctors/user/{user_id}/
class DoctorDetailByUserView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    lookup_field = 'user_id'

# --- WorkSchedule Views ---

# /api/doctors/{doctor_id}/schedules/
class WorkScheduleListCreateView(generics.ListCreateAPIView):
    serializer_class = WorkScheduleSerializer

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return WorkSchedule.objects.filter(doctor_id=doctor_id)

    def perform_create(self, serializer):
        doctor = get_object_or_404(Doctor, id=self.kwargs['doctor_id'])
        serializer.save(doctor=doctor)

# /api/doctors/{doctor_id}/schedules/{schedule_id}/
class WorkScheduleDetailView(generics.DestroyAPIView):
    serializer_class = WorkScheduleSerializer
    
    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return WorkSchedule.objects.filter(doctor_id=doctor_id)
    
    def get_object(self):
        queryset = self.get_queryset()
        schedule_id = self.kwargs['schedule_id']
        obj = get_object_or_404(queryset, id=schedule_id)
        return obj

# --- Availability Check View ---

# /api/doctors/{doctor_id}/availability/
class DoctorAvailabilityView(APIView):
    def get(self, request, doctor_id, *args, **kwargs):
        serializer = AvailabilityCheckSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        checked_dt = serializer.validated_data['datetime']
        day_of_week = checked_dt.weekday() # Monday is 0 and Sunday is 6
        checked_time = checked_dt.time()

        is_available = WorkSchedule.objects.filter(
            doctor_id=doctor_id,
            day_of_week=day_of_week,
            start_time__lte=checked_time,
            end_time__gte=checked_time
        ).exists()

        return Response({'is_available': is_available}, status=status.HTTP_200_OK)