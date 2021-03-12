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


class RouteRegistration(APIView):
    def post(self, request):
        route = RouteSerializer(data=request.data, context={"request": request})
        try:
            route.is_valid(raise_exception=True)
            route.save()
            return Response({"success": True})
        except Exception:
            return Response({"success": False})