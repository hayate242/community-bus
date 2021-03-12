from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bus.models import MasterBusStops, MasterRoutes


class BusStopDelete(APIView):
    def post(self, request):
        req_data = request.data
        bus_stop_id = req_data["bus_stop_id"]

        try:
            delete_bus_stop = MasterBusStops.objects.alive().filter(id=bus_stop_id)
            # idが存在しない場合のエラー処理
            if delete_bus_stop.count() == 0:
                return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
            else:
                routes = delete_bus_stop.prefetch_related('routes')[0].routes.alive()
                if routes.count() != 0:
                    return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
                delete_bus_stop.delete()
                return Response({"success": True})
        except:
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
