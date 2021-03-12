from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, date
import csv

from users.models import Users
from bus.models import *
from web.serializers import *
from mimaAPI.settings import BASE_DIR


class GetDriverList(APIView):
    def get(self, request):
        """
        # Response Example
        {
            "drivers": [
                {...},
                {
                    "driver_id": "2",
                    "driver_name": "向井くん",
                    "email": "mukai@example.com"
                }
            ]
        }
        """
        users = (
            Users.objects.prefetch_related("groups")
            .filter(is_active=True)
            .filter(groups__name="運転手")
        )
        resp_data = {}
        resp_data["drivers"] = [
            {
                "driver_id": f"{user.id}",
                "driver_name": user.username,
                "email": user.email,
            }
            for user in users
        ]
        return Response(resp_data)
