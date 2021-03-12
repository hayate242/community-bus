from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from bus import models


class BusStopSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    bus_stop_name = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    is_passing_point = serializers.BooleanField()
