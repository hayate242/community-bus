from rest_framework import serializers
from datetime import date


class MonthlyReportListSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()

    def validate(self, attrs):
        """年月のバリデーション"""
        year = attrs.get("year")
        month = attrs.get("month")
        try:
            date(year, month, 1)
        except ValueError as invalid_date:
            raise serializers.ValidationError("年月の指定が不適切です．") from invalid_date
        return attrs
