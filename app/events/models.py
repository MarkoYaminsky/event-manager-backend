from django.contrib.auth import get_user_model
from django.db import models

from app.common.models import BaseModel

User = get_user_model()


class Event(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="organized_events")
    invitees = models.ManyToManyField(User, related_name="invited_events", blank=True)

    def __str__(self):
        return self.title
