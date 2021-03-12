from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bus.models import MasterRoutes, RouteBusStops


class AllRoute(APIView):
    """
    # 路線一覧API
    ## Response 200 Example
    ```
    {
        "routes": [
            {
                "id": "1",
                "name": "hogehoge線",
                "route": [
                    {
                        "id": "1",
                        "name": "バス停1"
                    },
                    {...}
                ]
            },
            {...}
        ]
    }
    ```
    """

    def get(self, request):
        try:
            resp_data = {}
            resp_data["routes"] = [
                {
                    "id": f"{mr.id}",
                    "name": mr.route_name,
                    "used_by": [
                        course["course__course_name"] for course in mr.route_order_set
                        .select_related('course')
                        .filter(course__deleted_at__isnull=True)
                        .values("course", "course__course_name").distinct()
                    ],
                    "route": [
                        {
                            "id": f'{rbs.bus_stop_id}',
                            "name": rbs.bus_stop.bus_stop_name,
                            "order": f'{rbs.order}'
                        }
                        for rbs in RouteBusStops.objects.filter(route_id=mr.id).order_by("order")
                    ],
                }
                for mr in MasterRoutes.objects.alive().order_by('route_name')
            ]
            return Response(resp_data)
        except:
            return Response(resp_data, status.HTTP_400_BAD_REQUEST)
