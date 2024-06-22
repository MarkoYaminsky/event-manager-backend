from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from app.users.exceptions import InvalidCredentialsError
from app.users.types import UserAuthenticationTokenPair

User = get_user_model()


def get_all_users(*args: Q, **kwargs: Any) -> QuerySet[User]:
    return User.objects.filter(*args, **kwargs)


def create_user(username: str, password: str, **kwargs: Any) -> User:
    user = User.objects.create(username=username, **kwargs)
    user.set_password(password)
    user.save()
    return user


def login_user(username: str, password: str) -> UserAuthenticationTokenPair:
    user = get_all_users(username=username).first()

    if user is None or not user.check_password(password):
        raise InvalidCredentialsError

    return UserAuthenticationTokenPair(
        access_token=str(AccessToken.for_user(user)), refresh_token=str(RefreshToken.for_user(user))
    )
