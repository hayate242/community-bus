from rest_framework.views import APIView, Response
from rest_framework import status
from django.db.models import Sum, When, Case, Q, CharField, Value
from django.db.models.functions import Cast
from datetime import datetime, date, time

from bus.models import Boardings, WorkStartEnd, MasterRouteOrders, MasterBusStops, MasterBuses
from users.models import Users
from web.serializers.report.daily_report.daily_report_edit_serializer import DailyReportEditSerializer


class DailyReportUpdate(APIView):
    """
    日報情報保存（編集）API
    https://ictc.github.io/mima-community-bus-pbl2020-api-for-web/redoc-static.html#operation/post-api-v1-report-day
    """
    def post(self, request):
        try:
            payload = DailyReportEditSerializer(data=request.data, instance=Boardings.objects.none())
            payload.is_valid(raise_exception=True)
            payload.save()
            return Response({"success": True})
        except:
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
