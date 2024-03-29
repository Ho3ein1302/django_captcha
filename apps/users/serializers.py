from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.conf import settings

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .utils import get_tokens


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True, required=True)
    token = serializers.SerializerMethodField(read_only=True)
    captcha_key = serializers.CharField(write_only=True, required=True)
    captcha_value = serializers.CharField(write_only=True, required=True)

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
            'captcha_key',
            'captcha_value',
            'token',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        password = data['password']
        re_password = data['re_password']
        user_captcha_vlue = data['captcha_value']
        redis_captcha_value = settings.REDIS_CAPTCHA.get(data['captcha_key'])
        try:
            redis_captcha_value = redis_captcha_value.decode('utf-8')
        except Exception:
            raise ValidationError(_('incorrect captcha'))
        if user_captcha_vlue != redis_captcha_value:
            raise ValidationError(_('incorrect captcha'))
        else:
            if password != re_password:
                raise ValidationError(_('password and re_password must be match'))
            if password == re_password:
                return data
            else:
                raise ValidationError(_('something is wrong'))

    def get_token(self, obj):
        user = User.objects.get(id=obj.id)
        token = get_tokens(user)
        refresh = token['refresh']
        access = token['access']
        settings.REDIS_JWT_TOKEN.set(name=refresh, value=refresh, ex=settings.REDIS_REFRESH_TIME)
        return {'refresh': refresh, 'access': access}

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


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    captcha_key = serializers.CharField(write_only=True, required=True)
    captcha_value = serializers.CharField(write_only=True, required=True)
    token = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username',
                  'password',
                  'user',
                  'token',
                  'captcha_key',
                  'captcha_value']

    def validate(self, data):
        enter_password = data['password']
        user_captcha_vlue = data['captcha_value']
        redis_captcha_value = settings.REDIS_CAPTCHA.get(data['captcha_key'])
        try:
            redis_captcha_value = redis_captcha_value.decode('utf-8')
        except Exception:
            raise ValidationError(_('incorrect captcha'))
        if user_captcha_vlue != redis_captcha_value:
            raise ValidationError(_('incorrect captcha'))
        else:
            try:
                user = User.objects.get(
                    username=data['username']
                )
                if user.check_password(enter_password):
                    return data
                raise ValidationError(_('username or password are wrong'))
            except Exception:
                raise ValidationError(_('username or password are wrong'))

    def get_token(self, obj):
        user = User.objects.get(username=obj['username'])
        token = get_tokens(user)
        refresh = token['refresh']
        access = token['access']
        settings.REDIS_JWT_TOKEN.set(name=refresh, value=refresh, ex=settings.REDIS_REFRESH_TIME)
        return {'refresh': refresh, 'access': access}

    def get_user(self, obj):
        try:
            user = User.objects.get(username=obj['username'])
            user = UserSerializer(instance=user)
            return user.data
        except Exception:
            raise ValidationError(_('username or password is wrong'))


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        try:
            if settings.REDIS_JWT_TOKEN.get(data["refresh_token"]):
                settings.REDIS_JWT_TOKEN.delete(data["refresh_token"])
                return data
            else:
                raise ValidationError(_("invalid refresh_token or expired"))
        except Exception:
            raise ValidationError({_("error"): _('invalid refresh_token or expired')})

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Add or modify any custom representation logic here
        ret['msg'] = 'you have successfully log out'
        return ret


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(max_length=1000, required=True, label=_('refresh'), write_only=True)
    token = serializers.SerializerMethodField(read_only=True, label=_('token'))

    def validate_refresh(self, data):
        if settings.REDIS_JWT_TOKEN.get(name=data):
            return data
        else:
            raise ValidationError(_('Token is invalid or expired'))

    def get_token(self, obj):
        refresh = settings.REDIS_JWT_TOKEN.get(name=obj['refresh'])
        token_refresh = RefreshToken(refresh)
        user = User.objects.get(id=token_refresh['user_id'])
        settings.REDIS_JWT_TOKEN.delete(refresh)
        token = get_tokens(user)
        access = token['access']
        refresh = token['refresh']
        settings.REDIS_JWT_TOKEN.set(name=refresh, value=refresh, ex=settings.REDIS_REFRESH_TIME)
        data = {'access': access, 'refresh': refresh}
        return data
