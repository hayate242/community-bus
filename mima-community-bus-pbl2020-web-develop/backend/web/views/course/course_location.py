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


class CourseLocation(APIView):
    permission_classes = ()

    def get(self, request):
        """
        # バス路線位置情報取得API
        ## Response 200 Example
        ```
        {
            "routes": [
                {
                    "route_id": "1",
                    "route_name": "川之内線",
                    "bus_stops": [
                        {
                            "bus_stop_id": "1",
                            "bus_stop_name": "道の駅みま",
                            "latitude": "33.2862625",
                            "longitude": "132.5958557",
                            "is_passing_point": false
                        },
                        {...},
                    ]
                }
        }
        ```
        """
        resp_data = {
            "routes": [
                {
                    "route_id": f"{route.id}",
                    "route_name": route.route_name,
                    "bus_stops": [
                        {
                            "bus_stop_id": f"{bus_stop.bus_stop_id}",
                            "bus_stop_name": bus_stop.bus_stop.bus_stop_name,
                            "order": f"{bus_stop.order}",
                            "longitude": f"{MasterBusStops.objects.get(id=bus_stop.bus_stop_id).longitude}",
                            "latitude": f"{MasterBusStops.objects.get(id=bus_stop.bus_stop_id).latitude}",
                            "is_passing_point": MasterBusStops.objects.get(id=bus_stop.bus_stop_id).is_passing_point
                        }
                        for bus_stop in RouteBusStops.objects.filter(route=route.id).order_by("order")
                    ],
                }
                for route in MasterRoutes.objects.alive()
            ]
        }
        return Response(resp_data)
        # for route in MasterRoutes.objects.all():
        #     print(vars(route))
        #     for bus_stop in route.bus_stops.all():
        #         # print(vars(bus_stop))
        #         pass
        # return Response()
