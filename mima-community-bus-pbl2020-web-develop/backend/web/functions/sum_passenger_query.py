from django.db.models import When, Case, CharField, DateField, Sum, Q
from django.db.models.functions import Cast, Coalesce

from bus.models import WorkStartEnd


def SumPassengerQuery(group, *args):
    """乗客数の総数を返す"""
    condition = Q(fare__group=group)
    if 1 <= len(args):
        for item in args:
            condition |= Q(fare__group=item)
    return Cast(Sum(Case(When(condition, then='number'), default=0)),
                output_field=CharField())
