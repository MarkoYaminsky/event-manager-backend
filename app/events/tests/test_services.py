import datetime

import pytest

from app.events.models import Event
from app.events.services import (
    create_event,
    delete_event,
    get_event,
    get_future_events,
    set_invitees,
    update_event,
)
from app.events.tests.factories import EventFactory
from app.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def send_event_detail_email_mock(mocker):
    return mocker.patch("app.events.tasks.send_event_detail_email.delay")


class TestCreateEventService:
    title = "Birthday party"
    start_time = datetime.datetime.now()
    location = "Lviv"

    @pytest.fixture
    def set_invitees_mock(self, mocker):
        return mocker.patch("app.events.services.set_invitees")

    def test_without_invitees(self, user, set_invitees_mock):
        event = create_event(title=self.title, start_time=self.start_time, organizer=user, location=self.location)

        assert Event.objects.count() == 1
        assert event.title == self.title
        assert event.start_time == self.start_time
        assert event.location == self.location
        assert event.description == ""
        assert event.organizer == user
        assert event.end_time is None
        assert event.invitees.count() == 0
        set_invitees_mock.assert_not_called()

    def test_with_invitees(self, user, set_invitees_mock):
        invitee = UserFactory()

        event = create_event(
            title=self.title,
            start_time=self.start_time,
            organizer=user,
            invitees=[invitee],
        )

        set_invitees_mock.assert_called_once_with(event, [invitee])


class TestUpdateEventService:
    new_title = "new title"
    location = "Lviv"

    @pytest.fixture
    def set_invitees_mock(self, mocker):
        return mocker.patch("app.events.services.set_invitees")

    def test_without_invitees(self, set_invitees_mock):
        event = EventFactory(title="title", location=self.location)

        update_event(event=event, title=self.new_title)

        event.refresh_from_db()
        assert event.title == self.new_title
        assert event.location == self.location
        set_invitees_mock.assert_not_called()

    def test_with_invitees(self, set_invitees_mock):
        event = EventFactory()
        invitee = UserFactory()

        update_event(event=event, invitees=[invitee])

        set_invitees_mock.assert_called_once_with(event, [invitee])

    def test_with_invitees_unchanged(self, set_invitees_mock):
        invitee = UserFactory()
        event = EventFactory()
        event.invitees.set([invitee])

        update_event(event=event, invited_users=[invitee])

        set_invitees_mock.assert_not_called()

    def test_important_details_change(self, send_event_detail_email_mock):
        email = "example@gmail.com"
        event = EventFactory()
        invitee = UserFactory(email=email)
        event.invitees.add(invitee)

        update_event(event=event, location=self.location)

        send_event_detail_email_mock.assert_called_once_with(event.id, [invitee.email])


class TestDeleteEventService:
    def test_successful(self, mocker):
        send_event_deletion_email_mock = mocker.patch("app.events.tasks.send_event_deletion_email.delay")
        event = EventFactory()
        event_id = event.id

        delete_event(event)

        assert Event.objects.count() == 0
        send_event_deletion_email_mock.assert_called_once_with(event_id, [])


class TestGetFutureEventsService:
    def test_successful(self, user):
        event = EventFactory(start_time=datetime.datetime.now() + datetime.timedelta(days=1))
        event.invitees.add(user)
        late_event = EventFactory(start_time=datetime.datetime.now() - datetime.timedelta(days=1))
        late_event.invitees.add(user)
        EventFactory(organizer=user)

        future_events = get_future_events(user)

        assert future_events.count() == 1
        assert future_events.first() == event


class TestGetEventService:
    def test_successful(self):
        event = EventFactory()
        EventFactory()

        result = get_event(event.id)

        assert result == event


class TestSetInviteesService:
    def test_successful(self, send_event_detail_email_mock):
        event = EventFactory()
        invitee = UserFactory()

        set_invitees(event, [invitee])

        assert event.invitees.count() == 1
        assert event.invitees.first() == invitee
        send_event_detail_email_mock.assert_called_once_with(event.id, [])
