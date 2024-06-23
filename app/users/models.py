from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from app.common.models import BaseModel


class UserManager(BaseUserManager):
    def create_superuser(self, username: str, password: str) -> "User":
        from app.users.services import create_user

        return create_user(username=username, password=password, is_staff=True, is_superuser=True)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ("password",)
    objects = UserManager()

    def __str__(self) -> str:
        return self.username
