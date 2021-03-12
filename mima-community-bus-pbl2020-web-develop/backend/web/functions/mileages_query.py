from django.db.models import When, Case, CharField, Value, DateField, Max, Min
from django.db.models.functions import Cast, Coalesce

from bus.models import WorkStartEnd


def MileageQuery(date):
    # 業務開始・終了時のトリップメータ値
    return WorkStartEnd.objects.annotate(
        send_date=Cast("send_at", output_field=DateField())
    ).filter(
        send_date=date,
    ).values(
        "send_date", "bus_id", "course_id", "driver_id"
    ).annotate(
        mileage_start=Coalesce(Cast(
            Min(Case(
                When(work_start_end_flag=WorkStartEnd.FLAG.START,
                     then='trip_meter'))),
            output_field=CharField()), Value("")),
        mileage_end=Coalesce(Cast(
            Max(Case(
                When(work_start_end_flag=WorkStartEnd.FLAG.END,
                     then='trip_meter'), default=None)),
            output_field=CharField()), Value(""))
    )
