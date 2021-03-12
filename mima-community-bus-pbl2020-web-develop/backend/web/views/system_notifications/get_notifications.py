
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


class GetNotifications(APIView):
    permission_classes = ()
    """現在のお知らせを取得するAPI"""

    def get(self, request):
        """
        @summary: getアクセスを受けて，現在のお知らせ情報を返す
        @author:  Ibuki Onishi

        @param    request: nothing

        @return:  現在のお知らせ情報
        @rtype:   Object


        """
        notification = SystemNotifications.objects.order_by("id").values(
            "notification_message").last()

        # フロントに合わせてkey名を変更
        notification["message"] = notification.pop("notification_message")

        return Response(notification)
