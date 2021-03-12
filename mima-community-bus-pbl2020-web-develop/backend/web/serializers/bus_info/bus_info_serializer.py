from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from bus import models


class BusInfoSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    bus_name = serializers.CharField()
    bus_number = serializers.CharField()
