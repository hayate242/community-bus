from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer

from bus import models


class MonitoringHistorySerializer(serializers.Serializer):
    """
    # MonitorHistoryビュークラス用のシリアライザ
    ## Request Example
    ```
    {
        "start_date": "2020-10-12",
        "end_date": "2020-10-12"
    }
    ```
    """

    start_date = serializers.DateField()
    end_date = serializers.DateField()
