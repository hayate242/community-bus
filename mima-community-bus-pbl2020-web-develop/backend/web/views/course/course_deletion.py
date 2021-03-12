from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, date
import csv

from users.models import Users
from bus.models import *
from web.serializers.course.course_id_serializer import CourseIdSerializerForDel
from mimaAPI.settings import BASE_DIR


class CourseDeletion(APIView):
    """
    コース削除API
    """
    def post(self, request):
        try:
            course_id = CourseIdSerializerForDel(data=request.data)
            course_id.is_valid(raise_exception=True)
            course = course_id.validated_data.pop("course")
            #course.route_order_set.alive().delete()
            course.delete()
            return Response({"success": True})
        except:
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
