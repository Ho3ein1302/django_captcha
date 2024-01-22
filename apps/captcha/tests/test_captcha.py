from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
from model_bakery import baker


class GenerateCaptchaTest(APITestCase):

    def setUp(self):
        self.user = baker.make(get_user_model())

    def test_generate_captcha_success(self):
        url = reverse('captcha:generate_captcha')

        data = None
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertGreaterEqual(len(settings.REDIS_CAPTCHA.keys()), 1)

