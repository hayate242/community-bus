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


class MonitoringManageDelete(APIView):
    def post(self, request):
        req_data = request.data
        user_id = req_data["user_id"]

        # 削除箇所の特定
        target_data_id = UserCards.objects.get(pk=user_id).card_id
        parent_data_id = UserCards.objects.get(pk=user_id).user_id

        # 紐付けテーブルの削除処理
        try:
            delete_user_cards = UserCards.objects.filter(pk=user_id)

            # データが存在したときのみ削除処理
            if delete_user_cards.exists():
                delete_user_cards.delete()
        except:
            import traceback
            traceback.print_exc()
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

        # 見守り保護者の削除処理
        try:
            delete_parent_user = Users.objects.filter(
                pk=parent_data_id, groups__name=MONITOR_GROUP_NAME, is_active=True
            )

            # データが存在したときのみ削除処理
            if delete_parent_user.exists():
                delete_parent_user.update(is_active=False)

        except:
            import traceback

            traceback.print_exc()
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

        # 見守り対象の削除
        try:
            delete_target_user = MasterCards.objects.filter(pk=target_data_id)

            # データが存在したときのみ削除処理
            if delete_target_user.exists():
                delete_target_user.delete()

        except:
            import traceback
            traceback.print_exc()
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

        return Response({"success": True})
