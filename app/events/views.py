from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.events.serializers import (
    EventCreateInputSerializer,
    EventListOutputSerializer,
    EventRetrieveOutputSerializer,
    EventUpdateInputSerializer,
)
from app.events.services import (
    create_event,
    delete_event,
    get_future_events,
    update_event,
)


class OrganizedEventsListCreateApi(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventListOutputSerializer
    filter_backends = (SearchFilter,)
    search_fields = ("title", "description", "location")

    def get_queryset(self):
        return self.request.user.organized_events.order_by("-start_time")

    @extend_schema(request=EventCreateInputSerializer, responses=EventRetrieveOutputSerializer)
    def post(self, request, *args, **kwargs):
        serializer = EventCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        event = create_event(organizer=self.request.user, **serializer.validated_data)
        return Response(EventRetrieveOutputSerializer(event).data, status=status.HTTP_201_CREATED)


class EventRetrieveUpdateDestroyApi(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=EventRetrieveOutputSerializer)
    def get(self, request, event_id):
        event = get_object_or_404(get_future_events(self.request.user), id=event_id)
        serializer = EventRetrieveOutputSerializer(event)
        return Response(serializer.data)

    @extend_schema(request=EventUpdateInputSerializer(partial=True))
    def patch(self, request, event_id):
        event = get_object_or_404(get_future_events(self.request.user), id=event_id)
        serializer = EventUpdateInputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        update_event(event, **serializer.validated_data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, event_id):
        event = get_object_or_404(get_future_events(self.request.user), id=event_id)
        delete_event(event)
        return Response(status=status.HTTP_204_NO_CONTENT)


class InvitedEventsListApi(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EventListOutputSerializer
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ("title", "description", "location", "organizer__username")
    filterset_fields = ("organizer__username",)

    def get_queryset(self):
        return get_future_events(self.request.user).order_by("start_time")
