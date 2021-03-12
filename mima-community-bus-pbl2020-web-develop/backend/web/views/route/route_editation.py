from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bus.models import MasterRoutes
from web.serializers import RouteSerializer


class RouteEditation(APIView):
    def post(self, request):
        try:
            update_route = MasterRoutes.objects.get(id=request.data["id"])
            # 路線内で通過するバス停の変更は便にも影響する
            # 影響の出る便の取得
            route_order_set = update_route.route_order_set\
                .select_related('course')\
                .filter(course__deleted_at__isnull=True)
            # とりあえずは変更を許可しない
            # 宇和島市さんからの要望に応じて対応
            if route_order_set.count() != 0:
                return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
            route = RouteSerializer(
                data=request.data,
                context={"request": request},
                instance=update_route,
            )
            route.is_valid(raise_exception=True)
            route.save()
            return Response({"success": True})
        except:
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
