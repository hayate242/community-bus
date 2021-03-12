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


class AllCourse(APIView):
    def get(self, request):
        """
        # コース一覧取得
        ## Response 200 Example
        {
            "courses": [
                {
                    "id": "1",
                    "name": "Aコース",
                    "course": [
                        {
                            "id": "1",
                            "name": "hogehoge線",
                            "route": [
                                {
                                    "id": "1",
                                    "name": "バス停1",
                                    "time": "00:00",
                                    "is_used": true
                                },
                                {...}
                            ]
                        },
                        {...}
                    ]
                }
            ]
        }
        """
        resp_data = {"courses": []}
        try:
            for course in MasterCourse.objects.alive().order_by('course_name'):
                serializer = CourseSerializer(instance=course)
                resp_data["courses"].append(serializer.data)
            return Response(resp_data)
        except Exception:
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
