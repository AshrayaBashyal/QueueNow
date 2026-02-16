from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import SignupSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class SignupView(generics.CreateAPIView):
    """Handles user registration"""
    permission_classes = [permissions.AllowAny]
    serializer_class = SignupSerializer


class LoginView(TokenObtainPairView):
    """Handles JWT token generation(Email/Password)"""
    permission_classes = [permissions.AllowAny]


class RefreshTokenView(TokenRefreshView):
    """Handles JWT token refresh"""
    # Override the global IsAuthenticated setting.
    permission_classes = [permissions.AllowAny]    