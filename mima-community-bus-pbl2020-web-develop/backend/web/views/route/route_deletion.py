from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bus.models import MasterRoutes


class RouteDeletion(APIView):
    def post(self, request):
        try:
            route_id = request.data["route_id"]
            delete_route = MasterRoutes.objects.get(id=route_id)
            route_order_set = delete_route.route_order_set\
                .select_related('course')\
                .filter(course__deleted_at__isnull=True)
            if route_order_set.count() != 0:
                return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
            delete_route.delete()
            return Response({"success": True})
        except:
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
