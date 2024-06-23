from django.contrib.auth import get_user_model
from rest_framework import serializers

from app.events.models import Event
from app.users.services import get_all_users

User = get_user_model()


class EventListOutputSerializer(serializers.ModelSerializer):
    organizer_username = serializers.CharField(source="organizer.username")

    class Meta:
        model = Event
        fields = ("id", "title", "start_time", "end_time", "location", "organizer_username")


class InviteeOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class EventRetrieveOutputSerializer(serializers.ModelSerializer):
    organizer_username = serializers.CharField(source="organizer.username")
    invitees = InviteeOutputSerializer(many=True)

    class Meta:
        model = Event
        fields = "__all__"


class EventCreateInputSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(required=False)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField(required=False)
    location = serializers.CharField(required=False)
    invitees = serializers.ListSerializer(
        required=False,
        child=serializers.PrimaryKeyRelatedField(queryset=get_all_users()),
    )


class EventUpdateInputSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    location = serializers.CharField()
    invitees = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=get_all_users()))
