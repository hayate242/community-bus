from rest_framework import serializers

from bus.models import MasterCourse


class DailyReportListRequestSerializer(serializers.Serializer):
    date = serializers.DateField()
