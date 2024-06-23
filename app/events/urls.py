from django.urls import path

from app.events.views import (
    EventRetrieveUpdateDestroyApi,
    InvitedEventsListApi,
    OrganizedEventsListCreateApi,
)

app_name = "events"

urlpatterns = [
    path("organized/", OrganizedEventsListCreateApi.as_view(), name="organized-events-list-create"),
    path("invited/", InvitedEventsListApi.as_view(), name="invited-events-list"),
    path("<uuid:event_id>/", EventRetrieveUpdateDestroyApi.as_view(), name="event-retrieve-update-destroy"),
]
