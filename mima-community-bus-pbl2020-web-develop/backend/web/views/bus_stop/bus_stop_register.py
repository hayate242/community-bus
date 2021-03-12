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


class BusStopRegister(APIView):
    def post(self, request):
        req_data = request.data
        serializer = BusStopSerializer(data=req_data)  # serializerを利用したバリデーション

        if serializer.is_valid():
            MasterBusStops.objects.create(**serializer.validated_data)

        return Response({"success": serializer.is_valid()})
