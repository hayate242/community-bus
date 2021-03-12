from rest_framework import serializers

from bus.models import MasterRoutes, RouteBusStops
from web.serializers.route.route_bus_stops_serializer import RouteBusStopsSerializer


class RouteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(source="route_name")
    route = RouteBusStopsSerializer(source="relation_bus_stop", many=True)

    class Meta:
        model = MasterRoutes
        fields = "id", "user", "name", "route"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["id"] = f"{instance.route_id}"
        return representation

    def create(self, validated_data):
        # 経由するバス停情報を抜き出す
        bus_stop_data_set = validated_data.pop("relation_bus_stop")
        # 路線の登録
        route = super().create(validated_data)
        for bus_stop_data in bus_stop_data_set:
            # 路線内で経由するバス停の登録
            RouteBusStops.objects.create(
                route=route,
                bus_stop=bus_stop_data["bus_stop"],
                order=bus_stop_data["order"]
            )
        return route

    def update(self, instance, validated_data):
        instance.delete()
        return self.create(validated_data)
