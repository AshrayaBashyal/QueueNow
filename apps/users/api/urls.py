from django.urls import path
from .views import SignupView, LoginView, RefreshTokenView


app_name = 'users'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('login/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
]