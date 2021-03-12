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


class CourseEditation(APIView):
    """
    コース情報編集API
    ## Response 200 Example
    ```
    {
        "success": true
    }
    ```
    """

    def post(self, request):
        try:
            course_id = CourseIdSerializer(data=request.data)
            course_id.is_valid(raise_exception=True)
            course_up_to_date = CourseSerializer(
                data=request.data,
                context={"request": request},
                instance=MasterCourse.objects.alive().get(**course_id.validated_data),
            )
            course_up_to_date.is_valid(raise_exception=True)
            course_up_to_date.save()
            return Response({"success": True})
        except:
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
