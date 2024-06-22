import pytest
from django.contrib.auth import get_user_model

from app.users.exceptions import InvalidCredentialsError
from app.users.services import create_user, login_user
from app.users.tests.factories import UserFactory

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestCreateUserService:
    username = "username"
    password = "password"

    def test_successful(self):
        user = create_user(username=self.username, password=self.password)

        assert User.objects.first() == user


class TestLoginUserService:
    password = "some complex password"

    @pytest.fixture
    def user_with_password(self) -> User:
        user = UserFactory()
        user.set_password(self.password)
        user.save()
        return user

    def test_invalid_password(self, user_with_password):
        with pytest.raises(InvalidCredentialsError):
            login_user(username=user_with_password.username, password="1")

    def test_user_does_not_exist(self):
        with pytest.raises(InvalidCredentialsError):
            login_user(username="1ofr2ijfuh30q2=39fi30jv", password="Lorem Ipsum")

    def test_success(self, user_with_password):
        info = login_user(username=user_with_password.username, password=self.password)

        assert info.access_token is not None
        assert info.refresh_token is not None
