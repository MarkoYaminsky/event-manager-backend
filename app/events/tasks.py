from typing import List
from uuid import UUID

from app.common.emails import send_email
from app.event_manager.celery import app
from app.events.services import get_event


@app.task(ignore_result=True)
def send_event_detail_email(event_id: UUID, recipient_list: List[str]) -> None:
    event = get_event(event_id)
    send_email(
        subject=event.title,
        message=f"Details about event {event.title} have been updated! Go check it out!",
        recipient_list=recipient_list,
    )


@app.task(ignore_result=True)
def send_event_deletion_email(event_id: UUID, recipient_list: List[str]) -> None:
    event = get_event(event_id)
    send_email(
        subject=event.title,
        message=f"{event.title} has been canceled.",
        recipient_list=recipient_list,
    )
