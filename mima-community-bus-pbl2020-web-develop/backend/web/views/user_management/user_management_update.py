from django.db.models import Max
from django.contrib.auth.models import Group
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, date
import csv

from users.models import Users
from bus.models import *
from web.serializers import *
from mimaAPI.settings import BASE_DIR


class UserManagementUpdate(APIView):
    def post(self, request):
        req_data = request.data
        mail_add = req_data["email"]
        serializer = UserManagementSerializer(
            data=req_data, context={"mail_add": mail_add})
        user_id = req_data["id"]

        if serializer.is_valid():
            # 同じメールアドレスが存在し，かつそれが自分のものではない場合はエラーにする
            user_add = Users.objects.filter(
                email=serializer.validated_data["email"]).exclude(pk=user_id)
            if user_add.exists():
                return Response({"success": False, "message": "このメールアドレスは既に利用されています．"})

            update_user = Users.objects.filter(pk=user_id)

            # passwordが空のときの処理
            if serializer.validated_data["password"] == "":
                new_pass = update_user.get(pk=user_id).password
            else:
                new_pass = serializer.validated_data["password"]

            # グループ以外の編集
            user_data = {
                "username": serializer.validated_data["user_name"],
                "email": serializer.validated_data["email"],
                "password": new_pass
            }
            update_user.update(**user_data)

            # グループの編集
            user = Users.objects.get(id=user_id)
            group_id_list = [
                group for group in user.groups.all()
            ]
            current_group_object = group_id_list[0]

            # 現在のグループの削除
            current_group_object.user_set.remove(
                Users.objects.get(pk=user_id))

            # 新しいグループの追加
            regist_group = Group.objects.get(
                pk=serializer.validated_data["user_group_id"])
            regist_group.user_set.add(Users.objects.get(pk=user_id))

        return Response({"success": serializer.is_valid()})
