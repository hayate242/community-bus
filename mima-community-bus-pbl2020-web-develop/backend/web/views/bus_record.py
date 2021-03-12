from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, date
import csv

from users.models import Users
from bus.models import *
from web.serializers import *
from mimaAPI.settings import BASE_DIR
import datetime
from datetime import datetime as dt
import glob


class GetBusRecord(APIView):
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        """
        # バス停到着時刻取得API
        ## Request Example
        ```
        {
            "date": "2020-12-09",
        }
        ```
        ## Response 200 Example
        ```
        {
            "bus_record": [
                {
                    "id": "1",
                    "bus_stop": "バス停A",
                    "estimated_time": "12:30",
                    "arrival_time": "12:35"
                },
                {
                    "id": "2",
                    "bus_stop": "バス停B",
                    "estimated_time": "12:38",
                    "arrival_time": "12:42"
                }
            ]
        }
        ```
        """
        req_data = request.data
        req_data["date"] = datetime.datetime.strptime(
            request.data["date"], "%Y-%m-%d")
        print(req_data)

        csv_files = glob.glob(
            str(BASE_DIR) +
            f"/locations/arrival/{req_data['date'].strftime('%Y/%m/%d')}/*.csv"
        )

        resp_data = {}
        resp_data["bus_record"] = []
        for csv_file in csv_files:
            try:
                # csvファイルから，必要なresponseデータを作成
                bus_history = None
                with open(csv_file, encoding="utf8") as f:
                    reader = csv.DictReader(f)
                    # 全行読み込む
                    rows = [row for row in reader]
                    # 配列に追加
                    if req_data["selectDate"]:
                        bus_history = rows
                    else:
                        bus_history = [rows[-1]]
            except FileNotFoundError as e:
                return Response({"bus_record": []})

            result = []
            for index, data in enumerate(bus_history, 1):
                arrival_time = dt.strptime(
                    data["send_at"], "%Y-%m-%d %H:%M:%S")
                estimated_time = dt.strptime(
                    data["estimated_time"], "%H:%M:%S")
                resp_data["bus_record"].append(
                    {
                        "id": index,
                        "course_id": data["course_id"],
                        "bus_id": data["bus_id"],
                        "bus_stop": data["arrived_bus_stop_name"],
                        "bus_route": data["route_name"],
                        "estimated_time": f"{estimated_time.strftime('%H:%M')}",
                        "arrival_time": f"{arrival_time.strftime('%H:%M')}",
                    }
                )

        return Response(resp_data)
