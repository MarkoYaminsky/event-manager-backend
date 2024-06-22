from typing import NamedTuple

from django.contrib.auth import get_user_model

User = get_user_model()


class UserAuthenticationTokenPair(NamedTuple):
    access_token: str
    refresh_token: str
