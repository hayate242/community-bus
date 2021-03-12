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


class AllBusStop(APIView):
    def get(self, request):
        """
        # （全）バス停一覧取得API
        ## Response 200 Example
        ```
        {
            "bus_stop": [
                {
                    "id": "1",
                    "name": "バス停1",
                    "longitude": "111.222",
                    "latitude": "33.444"
                },
                {...}
            ]
        }
        ```
        """
        resp_data = {}
        resp_data["bus_stop"] = [
            {
                "id": f"{bus_stop.id}",
                "name": bus_stop.bus_stop_name,
                "longitude": f"{bus_stop.longitude}",
                "latitude": f"{bus_stop.latitude}",
                "is_passing_point": bus_stop.is_passing_point,
                "used_by": [
                    route["route_name"]
                    for route in bus_stop.routes.alive().values("id", "route_name").distinct()
                ]
            }
            for bus_stop in MasterBusStops.objects.alive().order_by('bus_stop_name')
        ]
        return Response(resp_data)
