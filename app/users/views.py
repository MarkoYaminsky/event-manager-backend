from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.users.serializers import (
    UserLoginInputSerializer,
    UserLoginOutputSerializer,
    UserRegistrationInputSerializer,
    UserRegistrationOutputSerializer,
)
from app.users.services import create_user, login_user


class UserLoginApi(APIView):
    serializer_class = UserLoginOutputSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserLoginInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        info = login_user(**serializer.validated_data)
        return Response(self.serializer_class(info).data, status=status.HTTP_200_OK)


class UserRegistrationApi(APIView):
    serializer_class = UserRegistrationOutputSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserRegistrationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user(**serializer.validated_data)
        return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
