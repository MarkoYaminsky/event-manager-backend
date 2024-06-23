import datetime
from typing import Any, List, Optional

from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from app.events.models import Event

User = get_user_model()


def create_event(
    title: str,
    start_time: datetime.datetime,
    organizer: User,
    location: str = "",
    description: str = "",
    end_time: Optional[datetime.datetime] = None,
    invitees: Optional[List[User]] = None,
) -> Event:
    event = Event.objects.create(
        title=title,
        description=description,
        start_time=start_time,
        end_time=end_time,
        location=location,
        organizer=organizer,
    )
    if invitees is not None:
        set_invitees(event, invitees)
    return event


def set_invitees(event: Event, invitees: List[User]) -> None:
    event.invitees.set(invitees)
    # TODO Send email: "Details about event {event.title} at have been updated! Go check it out!"


def update_event(
    event: Event,
    invitees: Optional[List[User]] = None,
    location: Optional[str] = None,
    start_time: Optional[datetime.datetime] = None,
    **kwargs: Any
) -> None:
    event_invitees = invitees or []

    for key, value in kwargs.items():
        if value is not None:
            setattr(event, key, value)
    event.save()

    if event.invitees.filter(id__in=[invitee.id for invitee in event_invitees]).count() != len(event_invitees):
        set_invitees(event, invitees)
        return
    if location != event.location or start_time != event.start_time:
        # TODO Send email
        ...


def delete_event(event: Event) -> None:
    event.delete()
    # TODO Send email


def get_future_events(user: User) -> QuerySet[Event]:
    return user.invited_events.filter(start_time__gte=datetime.datetime.now())
