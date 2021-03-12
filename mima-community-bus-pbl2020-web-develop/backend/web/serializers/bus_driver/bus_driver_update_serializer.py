from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from users.models import Users
from rest_framework import serializers, validators

from bus import models


class BusDriverUpdateSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    driver_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        required=False, allow_blank=True, allow_null=True)
