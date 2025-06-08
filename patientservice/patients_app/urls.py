from django.urls import path
from .views import PatientListCreateView, PatientDetailView, PatientDetailByUserView

urlpatterns = [
    path('', PatientListCreateView.as_view(), name='patient-list-create'),
    path('<uuid:id>/', PatientDetailView.as_view(), name='patient-detail'),
    path('user/<uuid:user_id>/', PatientDetailByUserView.as_view(), name='patient-detail-by-user'),
]