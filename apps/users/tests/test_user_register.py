# from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
# from model_bakery import baker

from .. import models


class UserRegisterTest(APITestCase):
    def setUp(self):
        url = reverse('captcha:generate_captcha')
        response = self.client.post(url, {}, follow=True)
        captcha_key = response.data['captcha']['CAPTCHA_KEY']
        captcha_value = settings.REDIS_CAPTCHA.get(captcha_key)
        captcha_value = captcha_value.decode('utf-8')
        self.url = reverse('users:user_register')
        self.data = {
            'first_name': 'hossein',
            'last_name': 'fatehi',
            'username': 'ho3ein1302',
            'phone': '09134575075',
            'email': 'hosseinfatehi1302@gmail.com',
            'password': 'password123',
            're_password': 'password123',
            'captcha_key': captcha_key,
            'captcha_value': captcha_value,
        }

    def test_user_register_success(self):
        response = self.client.post(self.url, self.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertGreaterEqual(models.User.objects.all().count(), 1)

    def test_user_register_invalidate_captcha(self):
        self.data['captcha_value'] = 331
        response = self.client.post(self.url, self.data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertGreaterEqual(models.User.objects.all().count(), 0)

    def test_user_register_invalidate_re_password(self):
        self.data['re_password'] = '12345677'
        response = self.client.post(self.url, self.data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertGreaterEqual(models.User.objects.all().count(), 0)

    def test_user_register_jwt_token(self):
        response = self.client.post(self.url, self.data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(settings.REDIS_JWT_TOKEN.get(response.data['token']['refresh']))
