from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from users.models import Users
from rest_framework import serializers, validators


from bus import models
import time


class UserManagementSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    user_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
    user_group_id = serializers.CharField()
