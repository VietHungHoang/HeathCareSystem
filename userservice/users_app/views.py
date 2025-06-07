from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import User, Role
from .serializers import UserSerializer, UserLoginSerializer

# /api/auth/register
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# /api/auth/login
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
                if user.password == password:
                    if not user.is_active:
                         return Response({"error": "Tài khoản đã bị vô hiệu hóa"}, status=status.HTTP_403_FORBIDDEN)
                    
                    response_data = {
                        "message": "Login successful",
                        "user_id": user.id,
                        "role_id": user.role.id
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Sai tài khoản hoặc mật khẩu"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"error": "Sai tài khoản hoặc mật khẩu"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# /api/users/
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

# /api/users/{user_id}/
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)