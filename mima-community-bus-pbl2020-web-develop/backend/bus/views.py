# 文字コード対策
from web.consts import DRIVER_GROUP_ID
from users.models import Users
from bus.serializers import *
from bus.models import *
from datetime import timedelta, datetime, date
from django.db.models import Max
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


class IsDriver(permissions.BasePermission):
    """
    check whether user is driver
    """

    def has_permission(self, request, view):
        try:
            driver_group = Group.objects.get(pk=DRIVER_GROUP_ID)
        except:
            return False

        return True if driver_group in request.user.groups.all() else False


class APIViewForiOS(APIView):
    permission_classes = (permissions.IsAuthenticated & IsDriver, )


class WorkStartEndView(APIViewForiOS):
    """
    業務開始・終了情報の保存（Bus Initial API）
    https://ictc.github.io/mima-community-bus-pbl2020-api-for-ios/#bus-initial-api-%E6%A5%AD%E5%8B%99%E9%96%8B%E5%A7%8B%E3%83%BB%E7%B5%82%E4%BA%86%E6%83%85%E5%A0%B1%E3%81%AE%E4%BF%9D%E5%AD%98-post
    """

    def post(self, request):
        req_data = request.data
        check_items = {
            "bus_id": "バスID",
            "driver_id": "運転手ID",
            "course_id": "コースID",
            "trip_meter": "トリップメーターの値",
            "money": "金額",
            "work_start_end_flag": "業務開始・終了フラグ",
            "send_at": "送信日時",
        }

        error_message = ""
        for key, val in check_items.items():
            if not req_data.get(key):
                if not error_message:
                    error_message += val
                else:
                    error_message += f",{val}"

        if error_message:
            error_message += "が渡されていません。"
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )

        req_data["bus"] = MasterBuses.objects.get(id=req_data.pop("bus_id"))
        req_data["course"] = MasterCourse.objects.get(
            id=req_data.pop("course_id"))
        req_data["driver"] = Users.objects.get(id=req_data.pop("driver_id"))
        WorkStartEnd.objects.create(**req_data)

        return Response({"success": "情報の保存に成功しました。"})


# バス点検情報の取得，保存(運転手，バス一覧，バス点検項目の登録)
class BusInspectionPostView(APIViewForiOS):
    def post(self, request):
        try:
            inspections = BusInspectionSerializer(data=request.data)
            inspections.is_valid(raise_exception=True)
            inspections.save()
            return Response({"success": "情報の保存に成功しました。"})
        except:
            return Response(
                {"error": "情報の保存に失敗しました。"}, status=status.HTTP_400_BAD_REQUEST
            )


class GetBusList(APIViewForiOS):
    def get(self, request):
        resp_data = {}
        routes = [route.as_dict() for route in MasterRoutes.objects.alive()]
        for route in routes:
            route_order_querys = MasterRouteOrders.objects.filter(
                route_id=route["route_id"]
            ).order_by("order")
            route_orders = [route_order.as_dict()
                            for route_order in route_order_querys]
            route["route_orders"] = route_orders

        resp_data["routes"] = routes

        return Response(resp_data)


class GetBusInspectionAPI(APIViewForiOS):
    def get(self, request):
        drivers = [
            {"driver_id": f"{driver.id}", "driver_name": driver.username}
            for driver in Users.objects.filter(groups=DRIVER_GROUP_ID, is_active=True)
        ]
        buses = [bus.as_dict() for bus in MasterBuses.objects.all()]

        resp_data = {}
        resp_data["drivers"] = drivers
        resp_data["buses"] = buses
        resp_data["item"] = [
            {"inspection_id": "1", "inspection_name": "燃料"},
            {"inspection_id": "2", "inspection_name": "エンジン"},
            {"inspection_id": "3", "inspection_name": "ブレーキ"},
            {"inspection_id": "4", "inspection_name": "ワイパー"},
            {"inspection_id": "5", "inspection_name": "クラクション"},
            {"inspection_id": "6", "inspection_name": "ウィンカー"},
            {"inspection_id": "7", "inspection_name": "灯火"},
            {"inspection_id": "8", "inspection_name": "ミラー"},
            {"inspection_id": "9", "inspection_name": "計器"},
            {"inspection_id": "10", "inspection_name": "タイヤ"},
            {"inspection_id": "11", "inspection_name": "排気音"},
            {"inspection_id": "12", "inspection_name": "冷却水"},
            {"inspection_id": "13", "inspection_name": "バッテリー"},
            {"inspection_id": "14", "inspection_name": "乗降ドア"},
            {"inspection_id": "15", "inspection_name": "車内点検"},
        ]

        return Response(resp_data)


class BusCourseList(APIView):

    # Web側でも使用している
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        resp_data = {}
        resp_data["Courses"] = [
            course.as_dict() for course in MasterCourse.objects.alive()
        ]

        return Response(resp_data)


class BusCourseInfo(APIViewForiOS):
    def post(self, request):
        deserializer = CourseInfoSerializer(data=request.data)
        if deserializer.is_valid():
            serializer = CourseInfoSerializer(
                instance=MasterCourse.objects.get(
                    **deserializer.validated_data)
            )
            return Response(serializer.data)
        else:
            routes = MasterRouteOrders.objects\
                .filter(course__in=MasterCourse.objects.alive())\
                .order_by("route", "order")
            serializer = RouteOrderSerializer(instance=routes, many=True)
            return Response({"course": serializer.data})


class BusStops(APIViewForiOS):
    def post(self, request):
        req_data = request.data
        check_items = {
            "route_id": "路線ID",
            "route_order_id": "便ID",
        }

        route = request.data.get("route_id")
        route_order = request.data.get("route_order_id")

        error_message = ""
        for key, val in check_items.items():
            if not req_data.get(key):
                if not error_message:
                    error_message += val
                else:
                    error_message += f",{val}"

        if error_message:
            error_message += "が渡されていません。"
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )

        resp_data = {}
        route_order_bus_stops = RouteOrderBusStops.objects.select_related(
            "route_bus_stop__bus_stop"
        ).filter(route_bus_stop__route_id=route, route_order_id=route_order)

        if not route_order_bus_stops.exists():
            error_message += "指定のコースに関する情報がありません。"
            return Response(
                {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
            )

        resp_data["bus_stops"] = [
            {
                "bus_stop_id": f"{route_order_bus_stop_route.route_bus_stop.bus_stop.id}",
                "bus_stop_order": f"{index}",
                "bus_stop_name": route_order_bus_stop_route.route_bus_stop.bus_stop.bus_stop_name,
                "longitude": f"{route_order_bus_stop_route.route_bus_stop.bus_stop.longitude}",
                "latitude": f"{route_order_bus_stop_route.route_bus_stop.bus_stop.latitude}",
            }
            for index, route_order_bus_stop_route in enumerate(route_order_bus_stops, 1)
        ]

        return Response(resp_data)


class BusFare(APIViewForiOS):
    def get(self, request):
        resp_data = {}
        try:
            # 運賃種別のリスト
            fares = dict([(
                enum.name,
                MasterFares.objects.alive().get(group=enum.value))
                for enum in MasterFares.GROUP])

            resp_data["table"] = [
                {
                    "row1_name": "降車数",
                    "row2": [
                        {
                            "row2_name": "",
                            "row3": [
                                {
                                    "row3_name": "",
                                    "fare_id": f"{fares['GET_OFF'].id}",
                                    "amount": f"{fares['GET_OFF'].amount}"
                                }
                            ],
                        },
                    ],
                },
                {
                    "row1_name": "乗車数",
                    "row2": [
                        {
                            "row2_name": "現金",
                            "row3": [
                                {
                                    "row3_name": "大人",
                                    "fare_id": f"{fares['CASH_ADULT'].id}",
                                    "amount": f"{fares['CASH_ADULT'].amount}"
                                },
                                {
                                    "row3_name": "小人",
                                    "fare_id": f"{fares['CASH_CHILD'].id}",
                                    "amount": f"{fares['CASH_CHILD'].amount}"
                                },
                                {
                                    "row3_name": "障大人",
                                    "fare_id": f"{fares['CASH_HANDICAPPED_ADULT'].id}",
                                    "amount": f"{fares['CASH_HANDICAPPED_ADULT'].amount}"
                                },
                                {
                                    "row3_name": "障小人",
                                    "fare_id": f"{fares['CASH_HANDICAPPED_CHILD'].id}",
                                    "amount": f"{fares['CASH_HANDICAPPED_CHILD'].amount}"
                                },
                            ],
                        },
                        {
                            "row2_name": "回数券",
                            "row3": [
                                {
                                    "row3_name": "大人",
                                    "fare_id": f"{fares['COUPON_ADULT'].id}",
                                    "amount": f"{fares['COUPON_ADULT'].amount}"
                                },
                                {
                                    "row3_name": "小人",
                                    "fare_id": f"{fares['COUPON_CHILD'].id}",
                                    "amount": f"{fares['COUPON_CHILD'].amount}"
                                },
                                {
                                    "row3_name": "障害者",
                                    "fare_id": f"{fares['COUPON_HANDICAPPED'].id}",
                                    "amount": f"{fares['COUPON_HANDICAPPED'].amount}"
                                },
                            ],
                        },
                        {
                            "row2_name": "定期券",
                            "row3": [
                                {
                                    "row3_name": "",
                                    "fare_id": f"{fares['COMMUTER_PASS'].id}",
                                    "amount": f"{fares['COMMUTER_PASS'].amount}"
                                },
                            ],
                        },
                        {
                            "row2_name": "無賃",
                            "row3": [
                                {
                                    "row3_name": "",
                                    "fare_id": f"{fares['FREE'].id}",
                                    "amount": f"{fares['FREE'].amount}"
                                },
                            ],
                        },
                    ],
                },
                {
                    "row1_name": "回数券の販売数",
                    "row2": [
                        {
                            "row2_name": "",
                            "row3": [
                                {
                                    "row3_name": "大人",
                                    "fare_id": f"{fares['COUPON_ADULT_SALE'].id}",
                                    "amount": f"{fares['COUPON_ADULT_SALE'].amount}"
                                },
                                {
                                    "row3_name": "小人",
                                    "fare_id": f"{fares['COUPON_CHILD_SALE'].id}",
                                    "amount": f"{fares['COUPON_CHILD_SALE'].amount}"
                                },
                                {
                                    "row3_name": "障害者",
                                    "fare_id": f"{fares['COUPON_HANDICAPPED_SALE'].id}",
                                    "amount": f"{fares['COUPON_HANDICAPPED_SALE'].amount}"
                                },
                            ],
                        },
                    ],
                },
            ]
            return Response(resp_data)
        except:
            return Response({"error": "error"})


class BusBoardingNumber(APIViewForiOS):
    def post(self, request):
        try:
            boarding_data = BoardingListSerializer(data=request.data)
            boarding_data.is_valid(raise_exception=True)
            boarding_data.save()
            return Response({"success": "情報の保存に成功しました。"})
        except:
            return Response({"error": "情報の保存に失敗しました。"})


class PostWatchOverBoarding(APIViewForiOS):
    def post(self, request):
        try:
            req_data = request.data
            check_items = {
                "driver_id": "運転手ID",
                "bus_id": "バスID",
                "card_id": "カードID",
                "bus_stop_id": "バス停ID",
                "send_at": "送信時間",
                "boarding_type": "乗降者種別",
            }

            error_message = ""
            for key, val in check_items.items():
                if not req_data.get(key):
                    if not error_message:
                        error_message += val
                    else:
                        error_message += f",{val}"

            if error_message:
                error_message += "が渡されていません。"
                return Response(
                    {"error": error_message}, status=status.HTTP_400_BAD_REQUEST
                )

            req_data["driver"] = Users.objects.get(
                id=req_data.pop("driver_id"))
            req_data["bus"] = MasterBuses.objects.get(
                id=req_data.pop("bus_id"))
            req_data["card"] = MasterCards.objects.get(
                id=req_data.pop("card_id"))
            req_data["bus_stop"] = MasterBusStops.objects.get(
                id=req_data.pop("bus_stop_id")
            )
            watch_over_boarding = WatchOverBoardings.objects.create(**req_data)

            return Response({"success": "情報の保存に成功しました。"})
        except:
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)


class SaveBusLocationView(APIViewForiOS):
    """
    バスロケーションの保存
    """

    def post(self, request):
        """
        ## Request Example
        ```
        {
            "bus_id": "1",
            "longitude": "33.687781",
            "latitude": "132.802734",
            "send_at": "2020-09-11 00:00:00",
            "route_name": "音地線",
            "vacancy_num": 6,
            "next_bus_stop_name": "三間小学校前"
        }
        ```
        """
        serializer = SaveBusLocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "バスロケーションの保存に成功しました。"})
        else:
            return Response(
                {"error": "バスロケーションの保存に失敗しました。"}, status=status.HTTP_400_BAD_REQUEST
            )


def daterange(_start, _end):
    yield _start
    for n in range((_end - _start).days):
        yield _start + timedelta(n)


class GetBusLocationView(APIViewForiOS):
    """バスロケーションの取得"""

    def get(self, request):
        """
        ## Response Example
        ```
        {
          "bus_id": "1",
          "locations": [
            {
              "date_time": "2020-09-11 00:00:00",
              "longitude": "33.687781",
              "latitude": "132.802734"
            }
          ]
        }
        ```
        """
        serializer = GetBusLocationSerializer(data=request.data)
        if serializer.is_valid():
            resp_data = {}
            bus_id = serializer.data["bus_id"]
            start_dt = datetime.strptime(
                serializer.data["start_from"], "%Y-%m-%d")
            end_dt = datetime.strptime(serializer.data["end_at"], "%Y-%m-%d")
            start = date(start_dt.year, start_dt.month, start_dt.day)
            end = date(end_dt.year, end_dt.month, end_dt.day)

            resp_data["bus_id"] = f"{bus_id}"
            resp_data["locations"] = []
            for ts_i in daterange(start, end):
                path = (
                    str(BASE_DIR)
                    + f"/locations/data/{ts_i.year}/{ts_i.month}/{ts_i.day}/{bus_id}.csv"
                )
                try:
                    with open(path, newline="", encoding="utf8") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            del row["bus_id"]
                            del row["created_at"]
                            row["date_time"] = row.pop("send_at")
                            resp_data["locations"].append(row)
                except FileNotFoundError:
                    pass
            return Response(resp_data)
        else:
            return Response({"error": "取得に失敗しました．"}, status=status.HTTP_400_BAD_REQUEST)


class CardInfo(APIViewForiOS):
    """カード情報の取得"""

    def get(self, request):
        """
        ## Response Example
        ```
        {
            "cards": [
                {
                    "card_id": "1",
                    "card_number": "112e4ce3af0d9a9e"
                },
                {
                    "card_id": "2",
                    "card_number": "012e4ce16ace5b31"
                }
            ]
        }
        ```
        """
        resp_data = {}
        resp_data["cards"] = [
            {"card_id": f"{card.id}", "card_number": f"{card.card_number}"}
            for card in MasterCards.objects.alive()
        ]

        return Response(resp_data)


class CardCreate(APIViewForiOS):
    """カード情報の取得"""

    def post(self, request):
        """
        ## Request Example
        ```
        {
            "bus_id": "1", #  <- Todo iPhoneとiPadの連携が取れていないのでわからないため現在は適当な値を格納．Phase2で修正
            "bus_stop_id": "1", # <- Todo iPhoneとiPadの連携が取れていないのでわからないため現在は適当な値を格納．Phase2で修正
            "driver_id": "1",
            "card_id": "1",
            "send_at": "2020-09-11 00:00:00",
            "boarding_type": "1"
        }
        ```
        ## 200 Response
        ```
        {
            "success": "saved information successfully"
        }
        ```
        """
        req_data = request.data
        # とりあえず，一番上のデータを取得する
        # Todo iPhone側で，どのバスか判定するようにする
        req_data["bus_id"] = MasterBuses.objects.all()[:1][0].id
        req_data["bus_stop_id"] = MasterBusStops.objects.all()[:1][0].id

        serializer = WatchOverBoardingsSerializer(data=req_data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success": "saved information successfully"})
        except Exception as e:
            print(dir(e))
            print(e.args)
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
