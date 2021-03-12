"""
運賃金額一覧API

# GET request

# response 200
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
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bus.models import MasterFares
from web.serializers.fare.fare_serializer import FareSerializer


class FareList(APIView):
    def get(self, request):
        queryset = MasterFares.objects.alive().exclude(amount=0)
        serializer = FareSerializer(many=True, instance=queryset)
        return Response(serializer.data)
