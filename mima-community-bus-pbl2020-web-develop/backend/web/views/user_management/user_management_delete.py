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


class UserManagementDelete(APIView):
    def post(self, request):
        req_data = request.data
        user_id = req_data["id"]
        try:
            delete_user = Users.objects.filter(pk=user_id)

            # データが存在したときのみ削除処理
            if delete_user.exists():
                delete_user.update(is_active=False)

            else:
                return Response({"success": False})

        except:
            import traceback

            traceback.print_exc()
            return Response({"success": False})

        return Response({"success": True})
