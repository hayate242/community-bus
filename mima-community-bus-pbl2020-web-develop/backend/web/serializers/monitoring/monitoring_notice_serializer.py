
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from bus import models


class MonitoringNoticeSerializer(serializers.Serializer):
    message = serializers.CharField()
