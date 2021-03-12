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


class UpdateNotifications(APIView):
    """お知らせ情報の更新処理"""

    def post(self, request):
        """
        @summary: 新しいお知らせ情報を受け取り，更新する
        @author:  Ibuki Onishi

        @param    request: {"notification": "新しいメッセージ"}
        @type:    JSON

        @return:  {"success": Bool}
        @rtype:   Object


        """
        req_data = request.data
        serializer = SystemNotificationSerializer(data=req_data)

        if serializer.is_valid():
            SystemNotifications.objects.update_or_create(
                pk=1,
                defaults={
                    "notification_message": serializer.validated_data["notification"]
                }
            )
        return Response({"success": serializer.is_valid()})
