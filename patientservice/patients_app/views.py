from rest_framework import generics
from .models import Patient
from .serializers import PatientSerializer

# /api/patients/
class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

# /api/patients/{patient_id}/
class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'id'

# /api/patients/user/{user_id}/
class PatientDetailByUserView(generics.RetrieveAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    lookup_field = 'user_id'