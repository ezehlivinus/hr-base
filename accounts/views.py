from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': True,
                'data': {
                    'auth_credentials': {
                        'refresh': str(refresh),
                        'access': str(refresh.token)
                    }
                }
            })
        return Response({
            'status': False,
            'message': 'Invalid credentials'
        }, status=status.HTTP_400_BAD_REQUEST)