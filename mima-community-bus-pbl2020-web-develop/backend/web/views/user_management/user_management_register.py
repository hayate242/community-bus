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


class UserManagementRegister(APIView):
    def post(self, request):
        req_data = request.data
        serializer = UserManagementSerializer(data=req_data)

        if serializer.is_valid():
            # 同じメールアドレスが存在し，かつそれが自分のものではない場合はエラーにする
            user_add = Users.objects.filter(email=serializer.validated_data["email"])
            if user_add.exists():
                return Response({"success": False, "message": "このメールアドレスは既に利用されています．"})

            try:
                user_data = {
                    "username": serializer.validated_data["user_name"],
                    "email": serializer.validated_data["email"],
                    "password": serializer.validated_data["password"],
                }
                user_group = Group.objects.get(
                    id=serializer.validated_data["user_group_id"]
                )
                user_group.user_set.add(Users.objects.create_user(**user_data))

            except:
                import traceback

                traceback.print_exc()
                return Response({"success": False})

        return Response({"success": serializer.is_valid()})
