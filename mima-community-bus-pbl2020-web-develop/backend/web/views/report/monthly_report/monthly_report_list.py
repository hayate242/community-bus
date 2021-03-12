from rest_framework.views import APIView, Response
from rest_framework import status
from django.db.models import Sum, When, Case, Q, CharField, Value, DateField, Max, Min, IntegerField, F, Subquery, OuterRef
from django.db.models.functions import Cast, Coalesce
from datetime import datetime, date, time
from calendar import monthrange

from bus.models import Boardings, WorkStartEnd, MasterRouteOrders, MasterBusStops, MasterBuses, MasterFares
from users.models import Users
from web.serializers.report.monthly_report.monthly_report_serializer import MonthlyReportListSerializer
from web.functions.sum_passenger_query import SumPassengerQuery


def SumFare(group, *args):
    """乗客数の総数を返す"""
    condition = Q(fare__group=group)
    if 1 <= len(args):
        for item in args:
            condition |= Q(fare__group=item)
    return Cast(Sum(Case(When(condition, then=F('number') * F('fare__amount')), default=0)),
                output_field=CharField())


class MonthlyReportList(APIView):
    def post(self, request):
        """
        月報情報取得API
        https://ictc.github.io/mima-community-bus-pbl2020-api-for-web/redoc-static.html#operation/get-api-v1-report-month
        """
        try:
            payload = MonthlyReportListSerializer(data=request.data)
            payload.is_valid(raise_exception=True)
            # 検索条件（日程）
            send_at_range = {
                'send_at__range': (
                    datetime.combine(
                        date(**payload.validated_data, day=1), time.min),
                    datetime.combine(
                        date(**payload.validated_data,
                             day=monthrange(**payload.validated_data)[1]),
                        time.max
                    )
                ),
            }

            # 月で利用されたコース一覧
            used_courses = WorkStartEnd.objects.filter(
                **send_at_range
            ).values(
                "course", "course__course_name"
            ).annotate(
                id=Cast(F("course_id"), output_field=CharField()),
                course_name=F("course__course_name")
            ).values(
                "id", "course_name"
            ).distinct().order_by("course")

            # 業務開始・終了時のトリップメータ値
            trip_meters = WorkStartEnd.objects.annotate(
                send_date=Cast("send_at", output_field=DateField())
            ).filter(
                send_date=OuterRef('send_date'),
                course=OuterRef('course'),
                bus=OuterRef('bus'),
                driver=OuterRef('driver'),
            ).values(
                # コース，バス，運転手別にした理由はなんかあったときのため
                "send_date", "course", "bus", "driver"
            ).annotate(
                trip_meter_start=Min(
                    Case(
                        When(work_start_end_flag=WorkStartEnd.FLAG.START, then="trip_meter")),
                    output_field=IntegerField()),
                trip_meter_end=Max(
                    Case(
                        When(work_start_end_flag=WorkStartEnd.FLAG.END, then="trip_meter")),
                    output_field=IntegerField())
            )

            # コースとコース毎の走行距離を求めるためのキーワード引数
            mileage_kwargs = dict([
                (
                    "mileage_{}".format(item["id"]),
                    Coalesce(
                        Sum(Case(When(course=item["id"], then=F(
                            "mileage_per_something"))), output_field=CharField(), distinct=True),
                        Value("0")
                    )
                ) for item in used_courses])

            # 月単位のコース別走行距離を求めるサブクエリ
            mileage_per_courses = WorkStartEnd.objects.annotate(
                send_date=Cast("send_at", output_field=DateField())
            ).filter(
                send_date=OuterRef('send_date')
            ).annotate(
                trip_meter_start=Subquery(
                    trip_meters.values("trip_meter_start")),
                trip_meter_end=Subquery(
                    trip_meters.values("trip_meter_end")),
                # something: バス，コース，運転手
                mileage_per_something=F(
                    'trip_meter_end') - F('trip_meter_start')
            ).values(
                "send_date", "bus", "course", "driver", "mileage_per_something"
            ).distinct().values(
                "send_date",
            ).annotate(
                **mileage_kwargs
            )

            # コースと対応するサブクエリの辞書
            subquery_kwargs = dict([
                (
                    "mileage_{}".format(item["id"]),
                    Subquery(mileage_per_courses.values(
                        "mileage_{}".format(item["id"])))
                ) for item in used_courses])

            # 日程毎の利用実績（降車・回数券販売は除く）
            monthly_number_of_users_report = Boardings.objects.filter(
                **send_at_range,
                fare__group__in=[
                    item for item in MasterFares.GROUP
                    if not any(map(item.value.endswith, ("降車", "回数券販売")))]
            ).annotate(
                send_date=Cast("send_at", output_field=DateField())
            ).values(
                "send_date"
            ).annotate(
                # 現金 大人
                cash_adult=SumPassengerQuery(MasterFares.GROUP.CASH_ADULT),
                # 現金 小人
                cash_child=SumPassengerQuery(MasterFares.GROUP.CASH_CHILD),
                # 現金 障害者
                cash_handicapped=SumPassengerQuery(
                    MasterFares.GROUP.CASH_HANDICAPPED_ADULT,
                    MasterFares.GROUP.CASH_HANDICAPPED_CHILD
                ),
                # 回数券 大人
                coupon_adult=SumPassengerQuery(MasterFares.GROUP.COUPON_ADULT),
                # 回数券 小人
                coupon_child=SumPassengerQuery(MasterFares.GROUP.COUPON_CHILD),
                # 回数券 障害者
                coupon_handicapped=SumPassengerQuery(
                    MasterFares.GROUP.COUPON_HANDICAPPED),
                # 回数券販売 大人
                coupon_adult_sale=SumPassengerQuery(
                    MasterFares.GROUP.COUPON_ADULT_SALE),
                # 回数券販売 小人
                coupon_child_sale=SumPassengerQuery(
                    MasterFares.GROUP.COUPON_CHILD_SALE),
                # 回数券販売 障害者
                coupon_handicapped_sale=SumPassengerQuery(
                    MasterFares.GROUP.COUPON_HANDICAPPED_SALE),
                # 定期券
                commuter_pass=SumPassengerQuery(
                    MasterFares.GROUP.COMMUTER_PASS),
                # 無賃
                free=SumPassengerQuery(MasterFares.GROUP.FREE),
                # 合計
                sum=Cast(Sum('number'), output_field=CharField()),
                # 走行距離
                **subquery_kwargs
            ).order_by('send_date')

            # 運賃の合計
            # 料金表でほしい運賃区分
            fare_groups_for_sum_of_fare = [
                item for item in MasterFares.GROUP
                if True in map(item.value.endswith, ['現金', '回数券販売'])]

            monthly_sum_of_fare_report = Boardings.objects.filter(
                **send_at_range,
                fare__group__in=fare_groups_for_sum_of_fare
            ).annotate(
                send_date=Cast("send_at", output_field=DateField())
            ).values(
                "send_date"
            ).annotate(
                # 現金 大人
                cash_adult=SumFare(MasterFares.GROUP.CASH_ADULT),
                # 現金 小人
                cash_child=SumFare(MasterFares.GROUP.CASH_CHILD),
                # 現金 障害者
                cash_handicapped=SumFare(
                    MasterFares.GROUP.CASH_HANDICAPPED_ADULT,
                    MasterFares.GROUP.CASH_HANDICAPPED_CHILD
                ),
                # 回数券販売 大人
                coupon_adult_sale=SumFare(MasterFares.GROUP.COUPON_ADULT_SALE),
                # 回数券販売 小人
                coupon_child_sale=SumFare(MasterFares.GROUP.COUPON_CHILD_SALE),
                # 回数券販売 障害者
                coupon_handicapped_sale=SumFare(
                    MasterFares.GROUP.COUPON_HANDICAPPED_SALE),
                # 合計（現金）
                cash_all=SumFare(*[
                    item for item in MasterFares.GROUP if item.value.endswith('現金')]),
                # 合計
                report_all=Cast(
                    Sum(F('number') * F('fare__amount')), output_field=CharField()),
            ).order_by('send_date')

            for item in monthly_number_of_users_report:
                item["day"] = str(item.pop("send_date").day)

            for item in monthly_sum_of_fare_report:
                item["day"] = str(item.pop("send_date").day)

            return Response({
                'monthly_number_of_users_report': monthly_number_of_users_report,
                'monthly_sum_of_fare_report': monthly_sum_of_fare_report,
                'courses': used_courses
            })
        except:
            return Response({'success': False}, status.HTTP_400_BAD_REQUEST)
