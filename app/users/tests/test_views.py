import pytest
from django.urls import reverse
from rest_framework import status

from app.users.tests.factories import UserFactory
from app.users.types import UserAuthenticationTokenPair

pytestmark = pytest.mark.django_db


class TestUserLoginApi:
    ROUTE = "users:login-user"
    access_token = "access"
    refresh_token = "refresh"
    password = "password"

    def test_success(self, api_client, mocker):
        user = UserFactory()
        login_user_mock = mocker.patch(
            "app.users.views.login_user",
            return_value=UserAuthenticationTokenPair(access_token=self.access_token, refresh_token=self.refresh_token),
        )

        response = api_client.post(reverse(self.ROUTE), data={"username": user.username, "password": self.password})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
        }
        login_user_mock.assert_called_with(username=user.username, password=self.password)


class TestUserRegistrationApi:
    ROUTE = "users:register-user"
    username = "username"
    password = "password"

    def test_success(self, api_client, mocker):
        user = UserFactory()
        register_user_mock = mocker.patch("app.users.views.create_user", return_value=user)

        response = api_client.post(reverse(self.ROUTE), data={"username": self.username, "password": self.password})

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {"id": str(user.id), "username": user.username}
        register_user_mock.assert_called_with(username=self.username, password=self.password)
