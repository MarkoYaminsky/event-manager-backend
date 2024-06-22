from factory import Sequence
from factory.django import DjangoModelFactory
from faker import Faker

from app.users.models import User

fake = Faker()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Sequence(lambda x: f"{fake.user_name()}{x}")
    password = "password"
