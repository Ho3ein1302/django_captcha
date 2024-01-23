# from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status
# from model_bakery import baker


class UserLoginTest(APITestCase):
    def setUp(self):
        self.url = reverse('users:user_login')
        url = reverse('captcha:generate_captcha')
        response = self.client.post(url, {}, follow=True)
        captcha_key = response.data['captcha']['CAPTCHA_KEY']
        captcha_value = settings.REDIS_CAPTCHA.get(captcha_key)
        captcha_value = captcha_value.decode('utf-8')
        url1 = reverse('users:user_register')
        data = {
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
        self.client.post(url1, data)
        self.data = {
            'username': 'ho3ein1302',
            'password': 'password123',
            'captcha_key': captcha_key,
            'captcha_value': captcha_value
        }

    def test_user_login_success(self):
        self.response = self.client.post(self.url, self.data)
        refresh = self.response.data['token']['refresh']
        self.assertEquals(self.response.status_code, status.HTTP_200_OK)
        self.assertTrue(settings.REDIS_JWT_TOKEN.get(refresh))

    def test_user_login_failed(self):
        self.data['password'] = 'wrong_password'
        response = self.client.post(self.url, self.data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_logout(self):
        url = reverse('users:user_logout')
        self.test_user_login_success()
        refresh = self.response.data['token']['refresh']
        data = {'refresh_token': refresh}
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertFalse(settings.REDIS_JWT_TOKEN.get(refresh))
