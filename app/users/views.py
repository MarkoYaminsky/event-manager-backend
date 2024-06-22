from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.users.serializers import (
    UserLoginOutputSerializer,
    UserLoginRegistrationInputSerializer,
    UserRegistrationOutputSerializer,
)
from app.users.services import create_user, login_user


class UserLoginApi(APIView):
    serializer_class = UserLoginOutputSerializer

    def post(self, request):
        serializer = UserLoginRegistrationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        info = login_user(**serializer.validated_data)
        return Response(self.serializer_class(info).data, status=status.HTTP_200_OK)


class UserRegistrationApi(APIView):
    serializer_class = UserRegistrationOutputSerializer

    def post(self, request):
        serializer = UserLoginRegistrationInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user(**serializer.validated_data)
        return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
