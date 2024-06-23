import datetime

from factory import LazyFunction, SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from app.events.models import Event
from app.users.tests.factories import UserFactory

fake = Faker()


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    title = fake.word()
    start_time = LazyFunction(lambda: datetime.datetime.now() + datetime.timedelta(days=1))
    organizer = SubFactory(UserFactory)
