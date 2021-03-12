from django.db.models import Max
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


class DriverUpdate(APIView):
    def post(self, request):
        req_data = request.data
        driver_id = req_data["driver_id"]
        serializer = BusDriverUpdateSerializer(data=req_data)

        if serializer.is_valid():
            # 同じメールアドレスが存在し，かつそれが自分のものではない場合はエラーにする
            user_add = Users.objects.filter(
                email=serializer.validated_data["email"]).exclude(pk=driver_id)
            if user_add.exists():
                return Response({"success": False, "message": "このメールアドレスは既に利用されています．"})

            update_driver = Users.objects.filter(
                groups__name=DRIVER_GROUP_NAME).filter(pk=driver_id)

            # idが存在し，かつグループが運転手のときのみ更新処理
            if update_driver.exists():
                # 更新用データの作成
                update_data = {
                    "username": serializer.validated_data["driver_name"],
                    "email": serializer.validated_data["email"],
                }

                # パスワード以外の更新処理
                update_driver.update(**update_data)

                # パスワードが空でないときのみ，パスワードを更新
                if serializer.validated_data["password"] != "":
                    # 新しいパスワードの設定
                    u = Users.objects.get(pk=driver_id)
                    u.set_password(serializer.validated_data["password"])
                    u.save()

        return Response({"success": serializer.is_valid() and update_driver.exists()})
