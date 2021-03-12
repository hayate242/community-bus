from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from bus.models import RouteOrderBusStops, MasterBusStops


class RouteOrderBusStopSerializer(serializers.ModelSerializer):
    """
    コース新規登録APIのRequestの内、2段目の入れ子のデータに使用
    """
    id = serializers.PrimaryKeyRelatedField(
        queryset=MasterBusStops.objects.all(),
        source="route_bus_stop.bus_stop"
    )
    time = serializers.TimeField(source="arrival_time")
    is_used = serializers.BooleanField(source="is_enabled")
    name = serializers.CharField(
        source="route_bus_stop.bus_stop.bus_stop_name", read_only=True
    )
    order = serializers.IntegerField(source="route_bus_stop.order")

    class Meta:
        model = RouteOrderBusStops
        fields = "id", "name", "time", "is_used", "order"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["id"] = f"{instance.route_bus_stop.bus_stop_id}"
        representation["order"] = f"{instance.route_bus_stop.order}"
        arrival_time = instance.arrival_time
        representation["time"] = (
            arrival_time.strftime("%H:%M") if arrival_time is not None else ""
        )
        return representation
