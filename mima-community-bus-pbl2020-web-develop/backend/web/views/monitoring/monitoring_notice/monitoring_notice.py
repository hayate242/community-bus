from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, date
import csv

from users.models import Users
from bus.models import *
from web.serializers import *
from mimaAPI.settings import BASE_DIR


class MonitoringNotice(APIView):
    def get(self, request):
        """
        # 見守り通知文API
        ## Response Example
        ```
        {
            "message": "{datetime}に{name}さんが「{bus-stop}」で乗車しました．"
        }
        ```
        """
        resp_data = {}
        try:
            resp_data["message"] = WatchingNotificationSentences.objects.get(
                pk=1
            ).sentence
        except WatchingNotificationSentences.DoesNotExist:
            resp_data = {"success": False}
        return Response(resp_data)