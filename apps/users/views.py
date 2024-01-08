from rest_framework import generics

from . import models
from . import serializers


class UserView(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()


class UserRegister(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    queryset = models.User.objects.all()