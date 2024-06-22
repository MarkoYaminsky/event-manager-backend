from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from app.users.views import UserLoginApi, UserRegistrationApi

app_name = "users"

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("login/", UserLoginApi.as_view(), name="login-user"),
    path("register/", UserRegistrationApi.as_view(), name="register-user"),
]
