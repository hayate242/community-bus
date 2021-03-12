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


class MonitoringNoticeUpdate(APIView):
    """見守り通知文の更新処理"""

    def post(self, request):
        """
        @summary: 見守り通知文の更新処理
        @author:  Ibuki Onishi

        @param    request: {"message": "String"}
        @type:    Object

        @return:  {"success": bool}
        @rtype:   Object
        """
        req_data = request.data
        serializer = MonitoringNoticeSerializer(data=req_data)

        if serializer.is_valid():
            WatchingNotificationSentences.objects.update_or_create(
                pk=1,
                defaults={
                    "sentence": serializer.validated_data["message"]
                }
            )
        return Response({"success": serializer.is_valid()})
