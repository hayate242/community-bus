from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from bus.models import MasterRoutes, MasterRouteOrders
from web.serializers.route.route_order_bus_stop_serializer import (
    RouteOrderBusStopSerializer,
)


class RouteOrderSerializer(WritableNestedModelSerializer):
    """
    コース新規登録APIのRequestの内、1段目の入れ子のデータに使用
    """
    id = serializers.PrimaryKeyRelatedField(queryset=MasterRoutes.objects.all(), source="route")
    name = serializers.CharField(source="route.route_name", read_only=True)
    route = RouteOrderBusStopSerializer(source="route_order_bus_stops_set", many=True)

    class Meta:
        model = MasterRouteOrders
        fields = "id", "name", "order", "route"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["id"] = f"{instance.route_id}"
        representation["order"] = f"{instance.order}"
        return representation