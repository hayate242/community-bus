from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from users.models import Users
from rest_framework import serializers, validators


from bus import models


class MonitoringManageSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=False)
    monitor_user_name = serializers.CharField()
    monitor_email = serializers.EmailField(source="email")
    card_number = serializers.CharField()
    monitor_target_user_name = serializers.CharField()
