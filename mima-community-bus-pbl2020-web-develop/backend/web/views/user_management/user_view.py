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
from web.consts import ADMIN_GROUP_NAME, DRIVING_COMPANY_GROUP_NAME


class UserView(APIView):
    def get(self, request):
        """
        # ユーザー情報管理API
        ## Response 200 Example
        ```
        {
            "users": [
                {
                    "id": "1",
                    "name": "test",
                    "email": "test@example.com"
                },
                {...}
            ]
        }
        ```
        """
        users = Users.objects.filter(is_active=True)
        resp_data = {}
        data = []
        for user in users:
            user_group_list = [group for group in user.groups.all()]

            # ictコースのアカウント以外のデータを格納
            if (
                user_group_list[0].name == ADMIN_GROUP_NAME
                or user_group_list[0].name == DRIVING_COMPANY_GROUP_NAME
            ):
                data.append(
                    {
                        "id": user.id,
                        "name": user.username,
                        "email": user.email,
                        "user_group_id": user_group_list[0].id,
                    }
                )
        resp_data["users"] = data
        return Response(resp_data)
