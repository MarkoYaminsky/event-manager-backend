import datetime

import pytest
from django.urls import reverse
from rest_framework import status

from app.events.models import Event
from app.events.tests.factories import EventFactory

pytestmark = pytest.mark.django_db


class TestOrganizedEventsListCreateApi:
    ROUTE = "events:organized-events-list-create"

    def test_list(self, authenticated_api_client):
        event = EventFactory(organizer=authenticated_api_client.user)

        response = authenticated_api_client.get(reverse(self.ROUTE))

        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()[0]
        assert response_json["id"] == str(event.id)
        assert response_json["organizer_username"] == authenticated_api_client.user.username

    def test_create(self, authenticated_api_client, mocker):
        event = EventFactory()
        title = "title"
        start_time = "2024-10-15T22:33:44Z"
        payload = {"title": title, "start_time": start_time}
        create_event_mock = mocker.patch("app.events.views.create_event", return_value=event)

        response = authenticated_api_client.post(reverse(self.ROUTE), data=payload)

        assert response.status_code == status.HTTP_201_CREATED
        response_json = response.json()
        assert response_json["id"] == str(event.id)
        create_event_mock.assert_called_once_with(
            title=title,
            organizer=authenticated_api_client.user,
            start_time=datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ"),
        )


class TestEventRetrieveUpdateDestroyApi:
    ROUTE = "events:event-retrieve-update-destroy"

    @pytest.fixture
    def event(self, authenticated_api_client) -> Event:
        event = EventFactory()
        event.invitees.add(authenticated_api_client.user)
        return event

    def test_retrieve(self, event, authenticated_api_client):
        response = authenticated_api_client.get(reverse(self.ROUTE, kwargs={"event_id": event.id}))

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["id"] == str(event.id)

    def test_partial_update(self, event, authenticated_api_client, mocker):
        new_title = "New title"
        update_event_mock = mocker.patch("app.events.views.update_event")

        response = authenticated_api_client.patch(
            reverse(self.ROUTE, kwargs={"event_id": event.id}), data={"title": new_title}
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        update_event_mock.assert_called_once_with(event, title=new_title)

    def test_delete(self, event, authenticated_api_client, mocker):
        delete_event_mock = mocker.patch("app.events.views.delete_event")

        response = authenticated_api_client.delete(reverse(self.ROUTE, kwargs={"event_id": event.id}))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        delete_event_mock.assert_called_once_with(event)


class TestInvitedEventsListApi:
    ROUTE = "events:invited-events-list"

    def test_list(self, authenticated_api_client):
        event = EventFactory()
        event.invitees.add(authenticated_api_client.user)

        response = authenticated_api_client.get(reverse(self.ROUTE))

        assert response.status_code == status.HTTP_200_OK
        response_json = response.json()[0]
        assert response_json["id"] == str(event.id)
