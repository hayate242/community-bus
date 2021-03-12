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


class BusesInfoDelete(APIView):
    """車両情報削除API"""

    def post(self, request):
        """
        @summary: postアクセスで車両情報の登録処理
        @author:  Ibuki Onishi

        @param    reauest: {"id": "String"}
        @type:    Object

        @return:  {"success": bool}
        @rtype:   Object


        """
        req_data = request.data
        bus_id = req_data["id"]

        try:
            delete_bus = MasterBuses.objects.filter(pk=bus_id)
            # idが存在しない場合の処理
            if delete_bus.count() == 0:
                return Response({"success": False})
            else:
                delete_bus.delete()
                return Response({"success": True})
        except:
            return Response({"success": False})
