from rest_framework.views import APIView, Response
from rest_framework import status
from django.views import View
from django.http import HttpResponse
from django.db.models import Sum, Q, CharField, Case, When, DateField
from django.db.models.functions import Cast
from datetime import date
from concurrent.futures import ThreadPoolExecutor, as_completed
import tablib
import io
import zipfile
import calendar

from bus.models import Boardings, MasterRouteOrders, MasterFares, MasterBuses, MasterRouteOrders, MasterBusStops
from users.models import Users
from web.serializers.report.monthly_report.monthly_report_serializer import MonthlyReportListSerializer
from web.functions.mileages_query import MileageQuery
from web.functions.sum_passenger_query import SumPassengerQuery


class DailyReportDownload(APIView):
    def post(self, request):
        payload = MonthlyReportListSerializer(data=request.data)
        payload.is_valid(raise_exception=True)
        year_month = payload.validated_data
        send_dates = [date(day=day, **year_month)
                      for day in range(1, calendar.monthrange(**year_month)[1] + 1)]

        files = {}
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.output_csv_per_day, send_date)
                       for send_date in send_dates]
            for future in as_completed(futures):
                # 処理が完了したものから取得
                day, csv_data = future.result()
                files["{:0>2}_日報".format(day)] = csv_data

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for name, data in files.items():
                zip_file.writestr(name + '.csv', data.encode('shift_jis'))
        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response["Content-Disposition"] = \
            "attachment; filename=\"{year:0>2}年{month:0>2}月宇和島市三間地区コミュニティバス日報.zip\"" \
            .format(**year_month)

        return response

    def output_csv_per_day(self, send_date):
        boardings = Boardings.objects.annotate(
            send_date=Cast("send_at", output_field=DateField())
        ).filter(
            send_date=send_date,
            fare__group__in=[
                item for item in MasterFares.GROUP
                if not item.value.endswith("回数券販売")]
        ).values(
            "bus", "route_order", "bus_stop", "driver", "bus_stop_order"
        ).annotate(
            # 現金 大人
            cash_adult=SumPassengerQuery(MasterFares.GROUP.CASH_ADULT),
            # 現金 小人
            cash_child=SumPassengerQuery(MasterFares.GROUP.CASH_CHILD),
            # 現金 障害者 大人
            cash_handicapped_adult=SumPassengerQuery(
                MasterFares.GROUP.CASH_HANDICAPPED_ADULT),
            # 現金 障害者 小人
            cash_handicapped_child=SumPassengerQuery(
                MasterFares.GROUP.CASH_HANDICAPPED_CHILD),
            # 回数券 大人
            coupon_adult=SumPassengerQuery(MasterFares.GROUP.COUPON_ADULT),
            # 回数券 小人
            coupon_child=SumPassengerQuery(MasterFares.GROUP.COUPON_CHILD),
            # 回数券 障害者
            coupon_handicapped=SumPassengerQuery(
                MasterFares.GROUP.COUPON_HANDICAPPED),
            # 定期券
            commuter_pass=SumPassengerQuery(MasterFares.GROUP.COMMUTER_PASS),
            # 無賃
            free=SumPassengerQuery(MasterFares.GROUP.FREE),
            # 降車
            get_off=SumPassengerQuery(MasterFares.GROUP.GET_OFF),
            # 合計
            sum=Cast(Sum(
                Case(
                    When(~Q(fare__group=MasterFares.GROUP.GET_OFF),
                         then='number'),
                    default=0)),
                output_field=CharField())
        )

        # 業務開始・終了時のトリップメータ値
        mileages = MileageQuery(send_date)

        for boarding in boardings:
            for mileage in mileages:
                route_order = MasterRouteOrders.objects.get(
                    id=boarding["route_order"])
                # バス，運転手，コースが同じトリップメータ値を追加
                if boarding["bus"] == mileage["bus_id"] \
                        and route_order.course_id == mileage["course_id"] \
                        and boarding["driver"] == mileage["driver_id"]:
                    boarding.update({
                        "mileage_start": mileage["mileage_start"],
                        "mileage_end": mileage["mileage_end"],
                    })
                    break
            else:
                raise Exception("乗降データがあるにもかかわらず業務開始データがない可能性があります．")

        # id からフィールドの値を求める
        # keyとcsvのヘッダーの合わせる
        for boarding in boardings:
            boarding["運転手"] = Users.objects.get(
                id=boarding.pop("driver")).username
            boarding["車両番号"] = MasterBuses.objects.get(
                id=boarding.pop("bus")).bus_number
            boarding["開始km"] = boarding.pop("mileage_start")
            boarding["終了km"] = boarding.pop("mileage_end")
            route_order = MasterRouteOrders.objects.get(
                id=boarding.pop("route_order"))
            boarding["コース名"] = route_order.course.course_name
            boarding["路線名"] = route_order.route.route_name
            boarding["便数"] = route_order.order
            boarding["停留所"] = MasterBusStops.objects.get(
                id=boarding.pop("bus_stop")).bus_stop_name
            boarding.pop("bus_stop_order")
            for item in MasterFares.GROUP:
                if not item.value.endswith("回数券販売"):
                    boarding[item.value] = boarding.pop(item.name.lower())
            boarding["計"] = boarding.pop("sum")

        headers = ["運転手", "車両番号", "開始km", "終了km", "コース名", "路線名", "便数", "停留所"]
        headers += [
            item.value for item in MasterFares.GROUP if not item.value.endswith("回数券販売")]
        headers.append("計")
        dataset = tablib.Dataset(headers=headers)
        for boarding in boardings:
            dataset.append(boarding.values())
        # print("!!check")

        return send_date.day, dataset.export('csv')
