from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import DEFAULTS
from rest_framework import serializers

from .models import Users


class LoginTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['access_token'] = data.pop('access')
        del data['refresh']

        data['token_type'] = 'Bearer'

        user_info = {f'{self.username_field}': attrs[self.username_field]}
        user = Users.objects.get(**user_info)
        data['user_id'] = f'{user.id}'
        data['user_name'] = user.username
        data['group'] = user.groups.last().name if user.groups.last() is not None else ""

        simple_jwt_settings = getattr(settings, 'SIMPLE_JWT', None)
        if simple_jwt_settings:
            data['expire_in'] = simple_jwt_settings.get(
                    'ACCESS_TOKEN_LIFETIME',
                    DEFAULTS['ACCESS_TOKEN_LIFETIME']
                ).total_seconds()

        return data


class UserSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='username')

    class Meta:
        model = Users
        fields = ['user_name', 'password', 'email', 'phone_number']

    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)
