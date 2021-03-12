from django.db.models import Max
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, date
import csv

from web.consts import *
from users.models import Users
from bus.models import *
from web.serializers import *
from mimaAPI.settings import BASE_DIR


class DriverDelete(APIView):
    def post(self, request):
        req_data = request.data
        driver_id = req_data["driver_id"]

        try:
            delete_driver = Users.objects.filter(id=driver_id)
            # idが存在しない場合のエラー処理
            if delete_driver.count() == 0:
                return Response({"success": False})
            # グループが運転手でなかった場合のみ削除
            elif delete_driver.filter(groups__name=DRIVER_GROUP_NAME).exists():
                delete_driver.update(is_active=False)
                return Response({"success": True})
            # 運転手以外のグループなら削除しない
            else:
                return Response({"success": False})
        except:
            return Response({"success": False})

        return Response({"success": True})
