from rest_framework.views import APIView, Response
from rest_framework import status
from django.db.models import Sum, When, Case, Q, CharField, Value, DateField, Max, Min, F
from django.db.models.functions import Cast, Coalesce
from datetime import datetime, date, time

from bus.models import Boardings, WorkStartEnd, MasterRouteOrders, MasterBusStops, MasterBuses, MasterFares
from users.models import Users
from web.serializers.report.daily_report.daily_report_list_serializer import DailyReportListRequestSerializer
from web.functions.mileages_query import MileageQuery


class DailyReportList(APIView):
    def post(self, request):
        """
        日報情報取得API
        https://ictc.github.io/mima-community-bus-pbl2020-api-for-web/redoc-static.html#operation/get-api-v1-report-day
        """
        try:
            payload = DailyReportListRequestSerializer(data=request.data)
            payload.is_valid(raise_exception=True)
            # 検索条件（コース・日程）
            send_at_date = payload.validated_data['date']
            send_at_range = {
                'send_at__range': (
                    datetime.combine(send_at_date, time.min),
                    datetime.combine(send_at_date, time.max)
                ),
            }

            boarding_query = Boardings.objects.filter(
                **send_at_range,
                fare__group__in=[
                    item for item in MasterFares.GROUP
                    if not item.value.endswith("回数券販売")]
            )

            # 乗車数（回数券購入を除く）
            boarding_data = boarding_query.select_related('fare')

            # 乗降数が記録してあるコースの一覧
            courses = boarding_query.annotate(name=F("route_order__course__course_name")).values(
                "name").distinct().order_by("name")

            # 業務開始・終了時のトリップメータ値
            mileages = MileageQuery(send_at_date)

            mileages_list = list(mileages)

            # 運賃区分の辞書
            fare_group_dict = dict([
                (item.value, item.name.lower())
                for item in MasterFares.GROUP
            ])

            boarding_data_values = boarding_data.values()
            # 日報
            daily_report = []
            # 乗降者数データの整形
            for boarding_datum in boarding_data_values:
                # 作成時間，更新時間，メモ
                # APIで利用されない
                boarding_datum.pop("created_at")
                boarding_datum.pop("updated_at")
                boarding_datum.pop("memo")

                # 乗降者数と運賃種別
                fare_id = boarding_datum.pop("fare_id")
                fare_group = MasterFares.objects.get(id=fare_id).group
                number = boarding_datum.pop("number")
                boarding_id = boarding_datum.pop("id")

                fare_type = fare_group_dict[fare_group]

                boarding_datum[fare_type] = {
                    "boarding_id": f'{boarding_id}',
                    "number": f'{number}'
                }

                # 日付
                send_at = boarding_datum.pop("send_at")
                boarding_datum["year"] = f'{send_at.year}'
                boarding_datum["month"] = f'{send_at.month}'
                boarding_datum["day"] = f'{send_at.day}'

                for row in daily_report:
                    # バス車両，便，バス停，運転手，路線内における経由順序
                    # 上記が一致するデータが存在するなら情報を追加
                    if boarding_datum["bus_id"] == row["bus_id"] \
                            and boarding_datum["route_order_id"] == row["route_order_id"] \
                            and boarding_datum["driver_id"] == row["driver_id"] \
                            and boarding_datum["bus_stop_id"] == row["bus_stop_id"] \
                            and boarding_datum["bus_stop_order"] == row["bus_stop_order"]:
                        diff_keys = boarding_datum.keys() - row.keys()
                        if fare_type in diff_keys:
                            if fare_type != "get_off":
                                boarding_datum["sum"] = row["sum"] + number
                            row.update(boarding_datum)
                            break
                else:
                    # バス車両，運転手，路線、バス停，経由順序が同じデータがなければ
                    # daily_report に追加
                    for item in mileages_list:
                        route_order = MasterRouteOrders.objects.get(
                            id=boarding_datum["route_order_id"])
                        # バス，運転手，コースが同じトリップメータ値を追加
                        if boarding_datum["bus_id"] == item["bus_id"] \
                                and route_order.course_id == item["course_id"] \
                                and boarding_datum["driver_id"] == item["driver_id"]:
                            boarding_datum.update({
                                "mileage_start": item["mileage_start"],
                                "mileage_end": item["mileage_end"],
                                "sum": number if fare_type != "get_off" else 0
                            })
                            break
                    else:
                        raise Exception("乗降データがあるにもかかわらず業務開始データがない可能性があります．")
                    daily_report.append(boarding_datum)

            # 合計を数字へ変換
            # 参照キーをオブジェクトの名前に変換等
            for row in daily_report:
                row["driver_name"] = Users.objects.get(
                    id=row.pop("driver_id")).username
                row["bus_number"] = MasterBuses.objects.get(
                    id=row.pop("bus_id")).bus_number
                route_order = MasterRouteOrders.objects.get(
                    id=row.pop("route_order_id"))
                row["route_order__order"] = "第{}便".format(route_order.order)
                row["route_name"] = route_order.route.route_name
                bus_stop = MasterBusStops.objects.get(
                    id=row.pop("bus_stop_id"))
                row["course_name"] = route_order.course.course_name
                row["bus_stop_name"] = bus_stop.bus_stop_name

                row["sum"] = str(row["sum"])
                row["bus_stop_order"] = str(row["bus_stop_order"])

            return Response({'dailyReport': daily_report, 'courses': [item["name"] for item in courses]})
        except:
            return Response({'success': False}, status.HTTP_400_BAD_REQUEST)
