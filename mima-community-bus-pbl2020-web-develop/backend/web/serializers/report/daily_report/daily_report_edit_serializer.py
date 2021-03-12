from rest_framework import serializers

from bus.models import MasterCourse, Boardings


class BoardingDataSerializer(serializers.Serializer):
    boarding_id = serializers.PrimaryKeyRelatedField(
        queryset=Boardings.objects.all(),
        source="boarding",
        allow_null=True
    )
    number = serializers.IntegerField()


class DailyReportSerializer(serializers.Serializer):
    get_off = BoardingDataSerializer()
    cash_adult = BoardingDataSerializer()
    cash_child = BoardingDataSerializer()
    cash_handicapped_adult = BoardingDataSerializer()
    cash_handicapped_child = BoardingDataSerializer()
    coupon_adult = BoardingDataSerializer()
    coupon_child = BoardingDataSerializer()
    coupon_handicapped = BoardingDataSerializer()
    commuter_pass = BoardingDataSerializer()
    free = BoardingDataSerializer()


class DailyReportEditSerializer(serializers.Serializer):
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=MasterCourse.objects.all(),
        source="course"
    )
    date = serializers.DateField()
    dailyReport = DailyReportSerializer(many=True)

    def update(self, instance, validated_data):
        daily_report = validated_data.pop("dailyReport")
        for daily_report_record in daily_report:
            # 乗客数の編集
            fare_types = [
                "get_off",
                "cash_adult",
                "cash_child",
                "cash_handicapped_adult",
                "cash_handicapped_child",
                "coupon_adult",
                "coupon_child",
                "coupon_handicapped",
                "commuter_pass",
                "free",
            ]

            for fare_type in fare_types:
                boarding = daily_report_record[fare_type]["boarding"]
                if boarding is not None:
                    boarding.number = daily_report_record[fare_type]["number"]
                    boarding.save()

        return Boardings.objects.none()
