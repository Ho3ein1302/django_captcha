from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from . import models
from . import serializers


class UserView(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()


class UserRegister(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    queryset = models.User.objects.all()


class UserLogin(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    queryset = models.User.objects.all()

    def post(self, request: Request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status.HTTP_200_OK)
