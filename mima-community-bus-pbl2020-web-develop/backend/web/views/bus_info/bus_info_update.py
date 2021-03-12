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


class BusesInfoUpdate(APIView):
    """車両情報更新API"""

    def post(self, request):
        """
        @summary: postアクセスで車両情報の更新処理
        @author:  Ibuki Onishi

        @param    reauest: {"id":"string", "bus_number": "string", "bus_name": "string"}
        @type:    Object

        @return:  {"success": bool}
        @rtype:   Object


        """
        req_data = request.data
        serializer = BusInfoSerializer(data=req_data)
        bus_id = req_data["id"]

        if serializer.is_valid():
            update_bus = MasterBuses.objects.filter(pk=bus_id)
            # idが存在しない場合の処理
            if update_bus.count() == 0:
                return Response({"success": False})
            else:
                update_bus.update(**serializer.validated_data)

        return Response({"success": serializer.is_valid()})
