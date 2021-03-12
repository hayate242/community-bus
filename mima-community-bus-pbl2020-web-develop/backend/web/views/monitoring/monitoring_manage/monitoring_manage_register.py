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


class MonitoringManageRegister(APIView):
    def post(self, request):
        req_data = request.data
        serializer = MonitoringManageSerializer(data=req_data)

        if serializer.is_valid():
            # 同じメールアドレスが存在し，かつそれが自分のものではない場合はエラーにする
            user_add = Users.objects.filter(
                email=serializer.validated_data["email"])
            if user_add.exists():
                return Response({"success": False, "message": "このメールアドレスは既に利用されています．"})

            # 見守り対象の登録
            try:
                target_data = {
                    "card_number": serializer.validated_data["card_number"],
                    "name": serializer.validated_data["monitor_target_user_name"]
                }
                target = MasterCards.objects.create(**target_data)
                target_id = target.pk
            except:
                import traceback
                traceback.print_exc()
                return Response({"success": False})

                # 見守り保護者の登録
            try:
                parent_data = {
                    "username": serializer.validated_data["monitor_user_name"],
                    "email": serializer.validated_data["email"],
                    # passwordは利用予定がないのでダミーの固定値を保存しています
                    "password": "Q3rZcVWy",
                }
                monitor_group = Group.objects.get(name=MONITOR_GROUP_NAME)
                monitor_group.user_set.add(
                    parent := Users.objects.create_user(**parent_data))
                parent_id = parent.pk

            except:
                import traceback
                traceback.print_exc()
                return Response({"success": False})

                # 紐付けテーブルの登録
            try:
                user_card_data = {
                    "card": target,
                    "user": parent
                }
                UserCards.objects.create(**user_card_data)
            except:
                return Response({"success": False})

        return Response({"success": serializer.is_valid()})
