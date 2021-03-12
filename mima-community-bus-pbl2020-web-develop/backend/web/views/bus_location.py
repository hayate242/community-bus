from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta, date
import csv
import datetime
import glob
import os

from users.models import Users
from bus.models import *
from web.serializers import *
from mimaAPI.settings import BASE_DIR


class BusLocation(APIView):
    """バスロケーション情報取得API"""

    permission_classes = ()

    def get(self, request):
        """
        @summary: getアクセス時の処理
        @author:  Ibuki Onishi

        @param    request: リクエストデータ
        @type:    Object

        @return:  バスロケーションデータ
        @rtype:   dict


        """
        # 今日の日付の取得
        today = datetime.datetime.today().strftime("%Y/%m/%d")

        # 今日送られてきたロケーション情報が保存されているcsv一覧を取得
        dir = str(BASE_DIR) + "/locations/data/" + today
        csv_files = glob.glob(dir + "/*.csv")

        # csvファイルから，必要なresponseデータを作成
        bus_locations = []
        for csv_file in csv_files:
            with open(csv_file, encoding="utf8") as f:
                reader = csv.DictReader(f)

                # 全行読み込む
                rows = [row for row in reader]

                # 最終行の取得
                response_data = rows[-1]

                # 不要データの削除
                response_data.pop("created_at")

                send_at = datetime.datetime.strptime(
                    response_data.pop("send_at"), '%Y-%m-%d %H:%M:%S')
                now = datetime.datetime.now()

                # send_atが今の時刻より1分以上前なら，translucent_flg=1,そうでなければtranslucent_flg=0を追加
                response_data["translucent_flg"] = "1" if now - \
                    send_at >= timedelta(minutes=1) else "0"

                # 路線の運行が終了していれば，次のbus_locationsへの配列の追加は行わないようにする
                arrival_data = str(BASE_DIR) + "/locations/arrival/" + \
                    today + "/" + response_data["course_id"] + ".csv"
                if os.path.exists(arrival_data):
                    with open(arrival_data, encoding="utf8") as af:
                        arrival_reader = csv.DictReader(af)
                        # 全行読み込む
                        arrival_rows = [a_row for a_row in arrival_reader]
                        # 最終行のnext_bus_stop_nameを取得
                        arrival_last_next_bus_stop = arrival_rows[-1]["next_bus_stop_name"]
                        # 到着時の次のバス停が存在しないときは，情報を送信しない
                        if arrival_last_next_bus_stop != "":
                            # 配列に追加
                            bus_locations.append(response_data)
                else:
                    # 配列に追加
                    bus_locations.append(response_data)

        return Response({"bus_locations": bus_locations})
