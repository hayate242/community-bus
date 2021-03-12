from rest_framework import serializers

from bus.models import MasterCourse, MasterRouteOrders, RouteOrderBusStops, RouteBusStops
from web.serializers.route.route_order_serializer import RouteOrderSerializer


class CourseSerializer(serializers.ModelSerializer):
    """
    コース新規登録APIで使用
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    name = serializers.CharField(source="course_name")
    course = RouteOrderSerializer(source="route_order_set", many=True)

    class Meta:
        model = MasterCourse
        fields = "id", "user", "name", "course"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["id"] = f"{instance.id}"
        return representation

    def create(self, validated_data):
        # 便情報を抜き取る
        route_order_data_set = validated_data.pop("route_order_set")
        # コースの作成
        course = super().create(validated_data)
        for route_order_data in route_order_data_set:
            # 経由するバス停情報を抜き取る
            bus_stop_data_set = route_order_data.pop("route_order_bus_stops_set")
            # 便の作成
            route_order = MasterRouteOrders.objects.create(**route_order_data, course=course)
            for bus_stop_data in bus_stop_data_set:
                RouteOrderBusStops.objects.create(
                    # 路線の経由するバス停情報
                    route_bus_stop=RouteBusStops.objects.get(
                        route=route_order.route,
                        bus_stop=bus_stop_data["route_bus_stop"]["bus_stop"],
                        order=bus_stop_data["route_bus_stop"]["order"],
                    ),
                    route_order=route_order,
                    arrival_time=bus_stop_data["arrival_time"],
                    is_enabled=bus_stop_data["is_enabled"],
                )
        return course

    def update(self, instance, validated_data):
        instance.delete()
        return self.create(validated_data)
