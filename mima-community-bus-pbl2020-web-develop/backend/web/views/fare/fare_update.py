"""
運賃金額更新API

# POST request
---
[
    {
        id: "1",
        type: "大人 - 現金",
        amount: 200
    },
    {
        id: "2",
        type: "小人 - 現金",
        amount: 100
    },
    ...
]
---

# response 200
---
{
    success: true
}
---
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bus.models import MasterFares
from web.serializers.fare.fare_serializer import FareSerializer


class FareUpdate(APIView):
    def post(self, request):
        serializer = FareSerializer(many=True, data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success": True})
        except:
            raise
            return Response({"success": False}, status.HTTP_400_BAD_REQUEST)
