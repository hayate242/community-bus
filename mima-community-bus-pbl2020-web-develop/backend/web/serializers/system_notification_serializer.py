from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from bus import models


class SystemNotificationSerializer(serializers.Serializer):
    notification = serializers.CharField()
