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


class DriverRegister(APIView):
    def post(self, request):
        req_data = request.data
        serializer = BusDriverSerializer(
            data=req_data)  # serializerを利用したバリデーション

        if serializer.is_valid():
            create_data = {
                "username": serializer.validated_data["driver_name"],
                "email": serializer.validated_data["email"],
                "password": serializer.validated_data["password"]
            }
            driver_group = Group.objects.get(name=DRIVER_GROUP_NAME)
            driver_group.user_set.add(Users.objects.create_user(**create_data))
            return Response({"success": True})

        else:
            if serializer.errors.get('email'):
                return Response({"success": False, "message": serializer.errors["email"][0]})
            else:
                return Response({"success": False})
