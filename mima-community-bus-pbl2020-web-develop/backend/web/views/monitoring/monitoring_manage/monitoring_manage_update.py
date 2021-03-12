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


class MonitoringManageUpdate(APIView):
    def post(self, request):
        req_data = request.data
        user_id = req_data["user_id"]
        serializer = MonitoringManageSerializer(data=req_data)

        if serializer.is_valid():
            # 更新箇所の特定
            target_data_id = UserCards.objects.get(pk=user_id).card_id
            parent_data_id = UserCards.objects.get(pk=user_id).user_id

            # 同じメールアドレスが存在し，かつそれが自分のものではない場合はエラーにする
            user_add = Users.objects.filter(
                email=serializer.validated_data["email"]).exclude(pk=parent_data_id)
            if user_add.exists():
                return Response({"success": False, "message": "このメールアドレスは既に利用されています．"})

            # 見守り対象の更新
            try:
                update_target_user = MasterCards.objects.filter(
                    pk=target_data_id)

                # データが存在したときのみ更新処理
                if update_target_user.exists():
                    target_data = {
                        "card_number": serializer.validated_data["card_number"],
                        "name": serializer.validated_data["monitor_target_user_name"]
                    }
                    update_target_user.update(**target_data)

                else:
                    return Response({"success": False})

            except:
                import traceback
                traceback.print_exc()
                return Response({"success": False})

            # 見守り保護者の更新
            try:
                update_parent_user = Users.objects.filter(pk=parent_data_id).filter(
                    groups__name=MONITOR_GROUP_NAME)

                # データが存在したときのみ更新処理
                if update_parent_user.exists():
                    parent_data = {
                        "username": serializer.validated_data["monitor_user_name"],
                        "email": serializer.validated_data["email"],
                        "password": "Q3rZcVWy",
                    }
                    update_parent_user.update(**parent_data)

                else:
                    import traceback
                    traceback.print_exc()
                    return Response({"success": False})

            except:
                import traceback
                traceback.print_exc()
                return Response({"success": False})

        return Response({"success": serializer.is_valid()})
