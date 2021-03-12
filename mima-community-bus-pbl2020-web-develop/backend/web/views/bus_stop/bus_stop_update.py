from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bus.models import MasterBusStops
from web.serializers import BusStopSerializer


class BusStopUpdate(APIView):
    def post(self, request):
        req_data = request.data
        serializer = BusStopSerializer(data=req_data)  # serializerを利用したバリデーション
        bus_stop_id = req_data["id"]

        if serializer.is_valid():
            update_bus_stop = MasterBusStops.objects.filter(id=bus_stop_id)
            # idが存在しない場合の処理
            if update_bus_stop.count() == 0:
                return Response({"success": False}, status.HTTP_400_BAD_REQUEST)

            update_bus_stop.update(**serializer.validated_data)

        return Response({"success": True})
