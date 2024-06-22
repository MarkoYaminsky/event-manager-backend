import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from app.users.tests.factories import UserFactory

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def authenticated_api_client(user, api_client) -> api_client:
    api_client.force_authenticate(user)
    return api_client
