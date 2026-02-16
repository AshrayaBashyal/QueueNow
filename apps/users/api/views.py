from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import SignupSerializer
from rest_framework_simplejwt.views import TokenObtainPairView 

class SignupView(generics.CreateAPIView):
    """Handles user registration"""
    permission_classes = [permissions.AllowAny]
    serializer_class = SignupSerializer


class LoginView(TokenObtainPairView):
    """Handles JWT token generation(Email/Password)"""
    permission_classes = [permissions.AllowAny]