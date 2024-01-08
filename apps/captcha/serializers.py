import uuid
import base64

from django.conf import settings

from rest_framework import serializers
from rest_captcha import captcha
from rest_captcha.settings import api_settings
from .utils import random_char_challenge


class GenerateCaptchaSerializer(serializers.Serializer):
    captcha = serializers.SerializerMethodField(read_only=True)

    def get_captcha(self, instance):
        key = str(uuid.uuid4())
        value = random_char_challenge(api_settings.CAPTCHA_LENGTH)
        settings.REDIS_CAPTCHA.set(key, value, settings.REDIS_CAPTCHA_TIME)
        image_bytes = captcha.generate_image(value)
        image_b64 = base64.b64encode(image_bytes)

        data = {
            'CAPTCHA_KEY': key,
            'CAPTCHA_IMAGE': image_b64,
            "image_type": "image/png",
            "image_decode": "base64",
            "value": value
        }
        return data
