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


class MonitoringManage(APIView):
    def get(self, request):
        """
        # 見守り管理API
        ## Response Example
        {
            "monitor_user": [
                {
                    "user_name": "uwajima",
                    "card_number": "12345678901234",
                    "create_at": "2020-10-13",
                    "last_use": "2020-10-13"
                },
                {...}
            ]
        }
        """
        user_cards = UserCards.objects.alive()
        watch_over_boarding_manage = WatchOverBoardings.objects
        resp_data = {}

        add_data = []  # resp_dataに格納するデータ用の一時変数
        for user_card in user_cards:  # 見守りユーザーのグループのみに絞り込み
            if user_card.user.groups.filter(name=MONITOR_GROUP_NAME).exists():
                if watch_over_boarding_manage.filter(card=user_card.card).exists():
                    last_used_date = f'{watch_over_boarding_manage.filter(card=user_card.card).aggregate(Max("send_at"))["send_at__max"].strftime("%Y-%m-%d")}'
                else:
                    last_used_date = "利用履歴なし"

                add_data.append(
                    {
                        "user_id": f"{user_card.id}",
                        "monitor_user_name": f"{user_card.user.username}",
                        "monitor_email": f"{user_card.user.email}",
                        "card_number": f"{user_card.card.card_number}",
                        "monitor_target_user_name": f"{user_card.card.name}",
                        "created_at": f'{user_card.created_at.strftime("%Y-%m-%d")}',
                        "last_used_date": last_used_date
                    }
                )

        resp_data["monitor_user"] = add_data

        return Response(resp_data)
