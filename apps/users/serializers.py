from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.conf import settings

from rest_framework import serializers


from .models import User
from .utils import get_tokens


class UserSerializer(serializers.Serializer):

    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True, required=True)
    captcha_key = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'phone',
            'email',
            'password',
            're_password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        password = data['password']
        re_password = data['re_password']

        if password != re_password:
            raise ValidationError(_('password and re_password must be match'))
        else:
            return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        user = User.objects.get(id=instance.id)
        token = get_tokens(user)
        refresh = token['refresh']
        access = token['access']
        settings.REDIS_JWT_TOKEN.set(name=refresh, value=refresh, ex=settings.REDIS_REFRESH_TIME)
        ret['token'] = {'access': access, 'refresh': refresh}
        return ret

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password']
        )
        return user
