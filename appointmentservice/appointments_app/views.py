import os
import requests
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer, AppointmentUpdateSerializer

class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = Appointment.objects.all()
        patient_id = self.request.query_params.get('patient_id')
        doctor_id = self.request.query_params.get('doctor_id')

        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        doctor_id = serializer.validated_data['doctor_id']
        appointment_time = serializer.validated_data['appointment_time']

        # # --- Bước 1: Gọi DoctorService để kiểm tra lịch làm việc ---
        # doctor_service_url = os.getenv('DOCTOR_SERVICE_URL')
        # if not doctor_service_url:
        #     return Response(
        #         {"error": "Doctor service URL is not configured."},
        #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
        #     )
        
        # availability_url = f"{doctor_service_url}/{doctor_id}/availability/"
        # params = {'datetime': appointment_time.isoformat()}
        
        # try:
        #     response = requests.get(availability_url, params=params)
        #     response.raise_for_status() # Ném lỗi nếu status code là 4xx hoặc 5xx
            
        #     availability_data = response.json()
        #     if not availability_data.get('is_available'):
        #         return Response(
        #             {"error": "Bác sĩ không có lịch làm việc vào thời gian này."},
        #             status=status.HTTP_400_BAD_REQUEST
        #         )
        # except requests.exceptions.RequestException as e:
        #     return Response(
        #         {"error": f"Không thể kết nối đến DoctorService: {e}"},
        #         status=status.HTTP_503_SERVICE_UNAVAILABLE
        #     )

        # # --- Bước 2: Kiểm tra xung đột lịch hẹn trong chính service này ---
        # is_slot_taken = Appointment.objects.filter(
        #     doctor_id=doctor_id,
        #     appointment_time=appointment_time,
        #     status='SCHEDULED'
        # ).exists()

        # if is_slot_taken:
        #     return Response(
        #         {"error": "Khung giờ này đã có người khác đặt."},
        #         status=status.HTTP_409_CONFLICT
        #     )
            
        # --- Bước 3: Nếu mọi thứ ổn, tạo lịch hẹn ---
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AppointmentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Appointment.objects.all()
    lookup_field = 'id'

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AppointmentUpdateSerializer
        return AppointmentSerializer

class AppointmentCancelView(generics.DestroyAPIView):
    queryset = Appointment.objects.all()
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'SCHEDULED':
            return Response(
                {"error": "Chỉ có thể hủy lịch hẹn đang được lên lịch."},
                status=status.HTTP_400_BAD_REQUEST
            )
        instance.status = 'CANCELED'
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)