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


class BusesInfo(APIView):
    def get(self, request):
        resp_data = {}
        buses = MasterBuses.objects.alive()
        resp_data["buses"] = [
            {
                "bus_id": f"{bus.id}",
                "bus_name": bus.bus_name,
                "bus_number": bus.bus_number,
            }
            for bus in buses
        ]
        return Response(resp_data)
