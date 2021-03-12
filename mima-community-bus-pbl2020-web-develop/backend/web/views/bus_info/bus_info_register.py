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


class BusesInfoRegister(APIView):
    """車両情報登録API"""

    def post(self, request):
        """
        @summary: postアクセスで車両情報の登録処理
        @author:  Ibuki Onishi

        @param    reauest: {"bus_number": "string", "bus_name": "string"}
        @type:    Object

        @return:  {"success": bool}
        @rtype:   Object


        """
        req_data = request.data
        serializer = BusInfoSerializer(data=req_data)

        if serializer.is_valid():
            MasterBuses.objects.create(**serializer.validated_data)

        return Response({"success": serializer.is_valid()})
