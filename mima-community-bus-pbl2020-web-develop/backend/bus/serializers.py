from django.db.models import Min, Case, When, Q
from rest_framework import serializers
from datetime import datetime, time
import os
import csv

from mimaAPI.settings import BASE_DIR
from bus import models
from users.models import Users
from web.consts import *
from geopy.distance import geodesic
from multiprocessing import Process
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False


class GetBusLocationSerializer(serializers.Serializer):
    """
    # バスロケーション取得API
    # Request Example
    ```
    {
      "bus_id": "1",
      "start_from": "2020-09-11",
      "end_at": "2020-09-11"
    }
    ```
    """

    bus_id = serializers.IntegerField()
    start_from = serializers.DateField()
    end_at = serializers.DateField()


class SaveBusLocationSerializer(serializers.Serializer):
    """[summary]
    バスロケーションの保存と，バス停通過時間の記録
    Args:
        serializers ([type]): [description]

    Returns:
        [type]: [description]
    """

    course_id = serializers.IntegerField()
    route_order_id = serializers.IntegerField()
    bus_stop_order = serializers.IntegerField()
    bus_id = serializers.IntegerField()
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()
    route_name = serializers.CharField()
    vacancy_num = serializers.IntegerField()
    next_bus_stop_name = serializers.CharField()
    send_at = serializers.DateTimeField()
    created_at = serializers.DateTimeField(default=datetime.now())

    def create(self, validated_data):
        bus_id = validated_data["bus_id"]
        ts = validated_data["send_at"]
        # どのバス停に着いたか判定する
        # 並列に実行
        p = Process(target=self.save_arrival, args=(validated_data,))
        p.start()
        self.save_data(validated_data, bus_id, ts)
        p.join()
        return 1

    def save_data(self, validated_data, bus_id, ts):
        # locationsアプリ内のデータディレクトリにcsvファイルを作成し、位置情報を保存する
        path = str(BASE_DIR) + f"/locations/data/{ts.strftime('%Y/%m/%d')}/"
        os.makedirs(path, exist_ok=True)
        with open(path + f"{bus_id}.csv", "a", encoding="utf8") as f:
            if f.tell() == 0:
                csv.writer(f).writerow([key for key in validated_data.keys()])
            csv.writer(f).writerow([val for val in validated_data.values()])

    def save_arrival(self, validated_data):
        """現在走っている路線のバス停の一覧を取得し，半径20m以内に近づいた場合に，データを保存する
        重複しているバス停は保存しないようにする
        /locations/arrival/{ts.year}/{ts.month}/{ts.day}/{course_id}.csv
        保存する項目，(course_id, route_order_id, bus_stop_order, bus_id, arrived_bus_stop_name, estimated_time, arrival_time, latitude, longitude, send_at, created_at)

        Args:
            validated_data ([type]): [description]
        """
        # データの一時保存
        arrival_data = validated_data
        arrival_data["estimated_time"] = ""
        arrival_data["arrived_bus_stop_name"] = ""
        # 保存先csvのpath
        arrival_path = (
            str(BASE_DIR)
            + f"/locations/arrival/{validated_data['send_at'].strftime('%Y/%m/%d')}/"
        )
        os.makedirs(arrival_path, exist_ok=True)
        # 項目名の保存
        with open(
            arrival_path + f"{validated_data['course_id']}.csv", "a", encoding="utf8"
        ) as f:
            if f.tell() == 0:
                csv.writer(f).writerow([key for key in arrival_data.keys()])
        # 不要なkeyの削除
        arrival_data.pop("arrived_bus_stop_name")

        # route_order_idに紐づいたバス停の一覧の取得
        serializer = RouteOrderSerializer(
            instance=models.MasterRouteOrders.objects.get(
                pk=validated_data["route_order_id"]
            )
        )
        # 現在位置と比較
        for bus_stop in serializer.data["bus_stops"]:
            bus_stop_lat_lng = (
                float(bus_stop["latitude"]),
                float(bus_stop["longitude"]),
            )
            current_lat_lng = (
                float(validated_data["latitude"]),
                float(validated_data["longitude"]),
            )
            # 距離の計算
            distance = geodesic(bus_stop_lat_lng, current_lat_lng).m
            # 距離がARRIVAL_DISTANCE以下ならarrival_dataに追加
            if distance < ARRIVAL_DISTANCE:
                arrival_data["estimated_time"] = bus_stop["arrival_time"]
                arrival_data["arrived_bus_stop_name"] = bus_stop["bus_stop_name"]
                break
        # 近くのバス停がない場合，return
        if "arrived_bus_stop_name" not in arrival_data:
            return

        # その日の初めての書き込みの場合は，補完を行わない
        if self.get_last_csv_data(arrival_path, validated_data) != []:

            # 同じbus_stop_ordreのバス停は保存しない
            if int(arrival_data["bus_stop_order"]) == int(self.get_last_csv_data(arrival_path, validated_data)[2]):
                return

                # bus_stop_orderが飛ばされていたら補完する
            elif int(arrival_data["bus_stop_order"]) != int(self.get_last_csv_data(arrival_path, validated_data)[2]) + 1:
                if arrival_data["bus_stop_order"] != 1:

                    # 到着判定が飛ばされた際の補完処理
                    # 補完処理が必要な回数だけループ
                    for i in range(int(validated_data["bus_stop_order"]) - int(self.get_last_csv_data(arrival_path, validated_data)[2]) - 1):
                        with open(arrival_path + f"{validated_data['course_id']}.csv", "a", encoding="utf8") as f:
                            # 補完データの作成
                            csv_completion_data = []
                            last_csv_data = self.get_last_csv_data(
                                arrival_path, validated_data)
                            # course_id
                            csv_completion_data.append(last_csv_data[0])
                            # route_order_id
                            csv_completion_data.append(last_csv_data[1])
                            # bus_stop_order
                            csv_completion_data.append(
                                int(last_csv_data[2]) + 1)
                            # bus_id
                            csv_completion_data.append(last_csv_data[3])
                            # longitude
                            csv_completion_data.append("")
                            # latitude
                            csv_completion_data.append("")
                            # route_name
                            csv_completion_data.append(last_csv_data[6])
                            # vacancy_num
                            csv_completion_data.append("")
                            # next_bus_stop_name
                            csv_completion_data.append(
                                models.RouteOrderBusStops.objects.filter(
                                    route_order=last_csv_data[1]).order_by("arrival_time")[int(last_csv_data[2])].route_bus_stop.bus_stop.bus_stop_name
                            )
                            # send_at
                            csv_completion_data.append(
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                            # created_at
                            csv_completion_data.append(datetime.now())
                            # estimated_time
                            csv_completion_data.append(
                                str(models.RouteOrderBusStops.objects.filter(
                                    route_order=last_csv_data[1]).order_by("arrival_time")[int(last_csv_data[2])].arrival_time
                                    ))
                            # arrived_bus_stop_name
                            csv_completion_data.append(last_csv_data[8])

                            # 補完データの書き込み
                            csv.writer(f).writerow(csv_completion_data)

        # データの追記
        with open(
            arrival_path + f"{validated_data['course_id']}.csv", "a", encoding="utf8"
        ) as f:
            csv.writer(f).writerow([val for val in arrival_data.values()])
        return

    def get_last_csv_data(self, arrival_path, validated_data):
        """最終行の情報を取得．同じなら書き込まない

        Args:
            arrival_path (string): csvまでのpath
        """
        with open(arrival_path + f"{validated_data['course_id']}.csv", "r") as f:
            next(csv.reader(f))
            csv_data = []
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                if row:  # avoid blank lines
                    csv_data.append(row)
        return csv_data[-1] if len(csv_data) > 0 else []


class RouteOrderBusStopSerializer(serializers.ModelSerializer):
    """
    コース情報取得APIのRequestの内、2段目の入れ子のデータに使用
    """

    bus_stop_id = serializers.IntegerField(
        source="route_bus_stop.bus_stop_id", read_only=True
    )
    bus_stop_name = serializers.CharField(
        source="route_bus_stop.bus_stop.bus_stop_name",
        read_only=True,
    )
    bus_stop_order = serializers.CharField(
        source="route_bus_stop.order", read_only=True
    )
    longitude = serializers.FloatField(
        source="route_bus_stop.bus_stop.longitude", read_only=True
    )
    latitude = serializers.FloatField(
        source="route_bus_stop.bus_stop.latitude", read_only=True
    )

    class Meta:
        model = models.RouteOrderBusStops
        fields = (
            "bus_stop_id",
            "bus_stop_name",
            "bus_stop_order",
            "longitude",
            "latitude",
            "arrival_time",
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["bus_stop_id"] = f"{instance.route_bus_stop.bus_stop_id}"
        representation["bus_stop_order"] = f"{instance.route_bus_stop.order}"
        representation["longitude"] = f"{instance.route_bus_stop.bus_stop.longitude}"
        representation["latitude"] = f"{instance.route_bus_stop.bus_stop.latitude}"
        return representation


class RouteOrderSerializer(serializers.Serializer):
    """
    コース情報取得APIのRequestの内、1段目の入れ子のデータに使用
    """
    route_id = serializers.IntegerField(read_only=True)
    route_name = serializers.CharField(
        source="route.route_name", read_only=True)
    route_order_id = serializers.IntegerField(source="id", read_only=True)
    route_order_name = serializers.IntegerField(source="order", read_only=True)
    bus_stops = serializers.SerializerMethodField()

    def get_bus_stops(self, instance):
        bus_stop_list = instance.route_order_bus_stops_set\
            .exclude(Q(arrival_time=time(0, 0)) |
                     Q(route_bus_stop__bus_stop__is_passing_point=True))\
            .order_by("arrival_time")
        return RouteOrderBusStopSerializer(instance=bus_stop_list, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["route_id"] = f"{instance.route_id}"
        representation["route_order_id"] = f"{instance.id}"
        representation["route_order_name"] = f"第{instance.order}便"
        return representation


class CourseInfoSerializer(serializers.ModelSerializer):
    """
    コース情報取得API
    """
    course_id = serializers.IntegerField(source="id", write_only=True)
    course = serializers.SerializerMethodField()

    class Meta:
        model = models.MasterCourse
        fields = "course_id", "course"

    def get_course(self, instance):
        route_id_list = instance.route_order_set.all()\
            .values("route_order_bus_stops_set__route_order")\
            .annotate(begin_at=Min(
                Case(
                    When(
                        route_order_bus_stops_set__arrival_time=time(0, 0),
                        then=None  # 集約関数はNullを無視する
                    ),
                    default="route_order_bus_stops_set__arrival_time"
                )))\
            .order_by("begin_at")

        route_list = [
            models.MasterRouteOrders.objects.get(
                id=route_id["route_order_bus_stops_set__route_order"]
            )
            for route_id in route_id_list
        ]

        return RouteOrderSerializer(instance=route_list, many=True).data


class BusInspectionSerializer(serializers.Serializer):
    bus_id = serializers.IntegerField()
    driver_id = serializers.IntegerField()
    checked = serializers.BooleanField()
    remark = serializers.CharField(max_length=1024, allow_blank=True)

    def create(self, validated_data):
        # check_tf_itemsは各点検項目が点検されたかを持つ
        check_tf_items = {
            "chack_fuel": "0",
            "chack_engine": "0",
            "chack_brake": "0",
            "chack_wiper": "0",
            "chack_horn": "0",
            "chack_turn_signal": "0",
            "chack_light": "0",
            "chack_mirror": "0",
            "chack_instrument": "0",
            "chack_tire": "0",
            "chack_exhaust_sound": "0",
            "chack_cooling_water": "0",
            "chack_battery": "0",
            "chack_door": "0",
            "chack_inside": "0",
        }

        if validated_data.pop("checked"):
            for key in check_tf_items:
                check_tf_items[key] = "1"

        validated_data["bus"] = models.MasterBuses.objects.get(
            id=validated_data.pop("bus_id")
        )
        validated_data["driver"] = Users.objects.get(
            id=validated_data.pop("driver_id"))
        validated_data.update(check_tf_items)
        return models.VehicleInspections.objects.create(**validated_data)


class BoardingSerializer(serializers.ModelSerializer):
    bus_id = serializers.PrimaryKeyRelatedField(
        queryset=models.MasterBuses.objects.all(), source="bus"
    )
    route_order_id = serializers.PrimaryKeyRelatedField(
        queryset=models.MasterRouteOrders.objects.all(), source="route_order"
    )
    bus_stop_id = serializers.PrimaryKeyRelatedField(
        queryset=models.MasterBusStops.objects.all(), source="bus_stop"
    )
    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=Users.objects.filter(groups=DRIVER_GROUP_ID), source="driver"
    )
    bus_stop_order = serializers.IntegerField()

    class Meta:
        model = models.Boardings
        fields = (
            "bus_id",
            # "route_id",
            "route_order_id",
            "bus_stop_id",
            "bus_stop_order",
            "driver_id",
            "fare_id",
            "number",
            "send_at",
        )

    def validate_fare_id(self, value):
        if value not in range(1, 14):
            raise serializers.ValidationError("fare_idが不正です。")
        return value


class BoardingListSerializer(serializers.Serializer):
    boardings = BoardingSerializer(many=True)

    def create(self, validated_data):
        for boarding in validated_data.pop("boardings"):
            instance = models.Boardings.objects.create(**boarding)
        return instance


class WatchOverBoardingsSerializer(serializers.ModelSerializer):
    """見守り情報登録Serializer
    Returns:
        serializer: 保存結果
    """

    card_id = serializers.PrimaryKeyRelatedField(
        queryset=models.MasterCards.objects.all(), source="card"
    )
    # card_id = serializers.CharField(source="card")
    bus_id = serializers.PrimaryKeyRelatedField(
        queryset=models.MasterBuses.objects.all(), source="bus"
    )
    bus_stop_id = serializers.PrimaryKeyRelatedField(
        queryset=models.MasterBusStops.objects.all(), source="bus_stop"
    )
    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=Users.objects.filter(groups=DRIVER_GROUP_ID), source="driver"
    )

    send_at = serializers.DateTimeField()
    boarding_type = serializers.CharField()

    class Meta:
        model = models.WatchOverBoardings
        fields = (
            "card_id",
            "bus_id",
            "bus_stop_id",
            "driver_id",
            "send_at",
            "boarding_type",
        )

    def create(self, validated_data):
        watch_orver_boarding = models.WatchOverBoardings(**validated_data)
        watch_orver_boarding.save()
        return watch_orver_boarding
