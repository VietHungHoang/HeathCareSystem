from django.urls import path
from .views import RegisterView, LoginView, UserListCreateView, UserDetailView

urlpatterns = [
    # Auth endpoints
    path('auth/register/', RegisterView.as_view(), name='user-register'),
    path('auth/login/', LoginView.as_view(), name='user-login'),

    # User management endpoints
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<uuid:id>/', UserDetailView.as_view(), name='user-detail'),
]