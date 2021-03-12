from django.db.models import Max
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, date
from web.consts import *

from bus.models import WatchOverBoardings
from web.serializers import MonitoringHistorySerializer


class MonitoringHistory(APIView):
    def post(self, request):
        """
        # 見守り履歴API
        ## Response Example
        {
        "history": [
            {
                "id": "1",
                "name": "uwajima",
                "date": "2020-10-12",
                "time": "12:00",
                "bus_stop": "停留所A",
                "type": "乗車"
            },
            {...}
        ]
        }
        """
        resp_data = {}
        serializer = MonitoringHistorySerializer(data=request.data)
        if serializer.is_valid():
            if request.data["selected_user"] != "":
                between = [
                    datetime(date.year, date.month, date.day, *(0, 0, 0))
                    for date in serializer.validated_data.values()
                ]
                between[1] += timedelta(hours=23, minutes=59, seconds=59)
                resp_data["history"] = [
                    {
                        "id": f"{wob.id}",
                        "name": wob.card.name,
                        "date": wob.send_at.strftime("%Y-%m-%d"),
                        "time": wob.send_at.strftime("%H:%M"),
                        "bus_stop": wob.bus_stop.bus_stop_name,
                    }
                    for wob in WatchOverBoardings.objects.select_related(
                        "card", "bus_stop"
                    ).filter(send_at__range=between).filter(card__name=request.data["selected_user"])
                ]
            else:
                between = [
                    datetime(date.year, date.month, date.day, *(0, 0, 0))
                    for date in serializer.validated_data.values()
                ]
                between[1] += timedelta(hours=23, minutes=59, seconds=59)
                resp_data["history"] = [
                    {
                        "id": f"{wob.id}",
                        "name": wob.card.name,
                        "date": wob.send_at.strftime("%Y-%m-%d"),
                        "time": wob.send_at.strftime("%H:%M"),
                        "bus_stop": wob.bus_stop.bus_stop_name,
                    }
                    for wob in WatchOverBoardings.objects.select_related(
                        "card", "bus_stop"
                    ).filter(send_at__range=between)
                ]

        else:
            return Response({"error": "取得に失敗しました．"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(resp_data)
