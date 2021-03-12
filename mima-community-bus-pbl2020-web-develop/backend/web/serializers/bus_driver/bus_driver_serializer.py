from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from users.models import Users
from rest_framework import serializers, validators

from bus import models


class BusDriverSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    driver_name = serializers.CharField()
    email = serializers.EmailField(validators=[validators.UniqueValidator(
        queryset=Users.objects.all(), message="このメールアドレスは既に使用されています．")])
    password = serializers.CharField()
