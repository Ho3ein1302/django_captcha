from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from .serializers import GenerateCaptchaSerializer


class GenerateCaptchaView(GenericAPIView):
    serializer_class = GenerateCaptchaSerializer

    def post(self, request):
        serializer = self.serializer_class(request.data)
        return Response(serializer.data, status.HTTP_200_OK)
