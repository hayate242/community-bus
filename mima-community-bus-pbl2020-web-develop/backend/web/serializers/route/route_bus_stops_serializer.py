from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from bus.models import MasterBusStops, RouteBusStops


class RouteBusStopsSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=MasterBusStops.objects.alive(),
        source="bus_stop"
    )
    name = serializers.CharField(source="bus_stop.bus_stop_name", read_only=True)

    class Meta:
        model = RouteBusStops
        fields = "id", "name", "order"
