import datetime
from typing import Any, List, Optional
from uuid import UUID

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
    from app.events.tasks import send_event_detail_email

    event.invitees.set(invitees)
    send_event_detail_email.delay(event.id, [invitee.email for invitee in invitees if invitee.email])


def update_event(event: Event, invitees: Optional[List[User]] = None, **kwargs: Any) -> None:
    from app.events.tasks import send_event_detail_email

    location = kwargs.get("location")
    start_time = kwargs.get("start_time")
    event_invitees = invitees or []

    if event.invitees.filter(id__in=[invitee.id for invitee in event_invitees]).count() != len(event_invitees):
        set_invitees(event, invitees)
        return
    if location is not None and location != event.location or start_time is not None and start_time != event.start_time:
        send_event_detail_email.delay(event.id, [invitee.email for invitee in event.invitees.all()])

    for key, value in kwargs.items():
        if value is not None:
            setattr(event, key, value)
    event.save()


def delete_event(event: Event) -> None:
    from app.events.tasks import send_event_deletion_email

    send_event_deletion_email.delay(event.id, [invitee.email for invitee in event.invitees.all()])
    event.delete()


def get_future_events(user: User) -> QuerySet[Event]:
    return user.invited_events.filter(start_time__gte=datetime.datetime.now())


def get_event(event_id: UUID) -> Event:
    return Event.objects.get(id=event_id)
