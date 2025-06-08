from django.urls import path
from .views import (
    DoctorListCreateView,
    DoctorDetailView,
    DoctorDetailByUserView,
    WorkScheduleListCreateView,
    WorkScheduleDetailView,
    DoctorAvailabilityView
)

urlpatterns = [
    # Doctor endpoints
    path('', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('<uuid:id>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('user/<uuid:user_id>/', DoctorDetailByUserView.as_view(), name='doctor-detail-by-user'),
    
    # Schedule endpoints nested under a doctor
    path('<uuid:doctor_id>/schedules/', WorkScheduleListCreateView.as_view(), name='schedule-list-create'),
    path('<uuid:doctor_id>/schedules/<int:schedule_id>/', WorkScheduleDetailView.as_view(), name='schedule-detail'),
    
    # Availability check endpoint
    path('<uuid:doctor_id>/availability/', DoctorAvailabilityView.as_view(), name='doctor-availability'),
]