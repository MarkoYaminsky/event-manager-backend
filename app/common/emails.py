from typing import List

from django.conf import settings
from django.core.mail import send_mail


def send_email(subject: str, message: str, recipient_list: List[str]) -> None:
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
    )
