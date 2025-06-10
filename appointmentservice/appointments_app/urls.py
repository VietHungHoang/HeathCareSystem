from django.urls import path
from .views import AppointmentListCreateView, AppointmentDetailView, AppointmentCancelView

urlpatterns = [
    path('', AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('<uuid:id>/', AppointmentDetailView.as_view(), name='appointment-detail'),
    path('cancel/<uuid:id>/', AppointmentCancelView.as_view(), name='appointment-cancel'),

]