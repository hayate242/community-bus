<template>
  <div>
    <div class="select-area">
      <Mt15>
        <div
          class="flex flex-between md-layout-item md-medium-size-100 md-size-100"
        >
          <div class="flex">
            <div>
              <p>日付を選択してください</p>
              <VueCtkDateTimePicker
                v-model="selectedDate"
                label="日付"
                format="YYYY-MM-DD"
                formatted="YYYY-MM-DD"
                position="bottom"
                overlay
                only-date
                noClearButton
              />
            </div>
            <div class="ml-15">
              <p>コースを選択してください</p>
              <md-field class="mt-n13">
                <!-- <label>コースを選択</label> -->
                <md-select v-model="selectedCourse">
                  <md-option
                    v-for="(course, index) in courses"
                    :key="index"
                    :value="course"
                    >{{ course }}</md-option
                  >
                </md-select>
              </md-field>
            </div>
          </div>
          <div class="flex">
            <div v-if="editMode">
              <md-button
                class="md-warning download-button"
                @click="
                  changeEditMode();
                  updateReport();
                "
                >確定</md-button
              >
            </div>
            <div v-else>
              <md-button
                class="md-info download-button"
                @click="changeEditMode()"
                >編集</md-button
              >
            </div>
            <div class="ml-15" v-if="editMode">
              <md-button
                class="download-button"
                @click="
                  changeEditMode();
                  cancelEdit();
                "
                >キャンセル</md-button
              >
            </div>
            <div class="ml-15" v-else>
              <md-button
                class="md-primary download-button"
                @click="showDownloadModal"
                >ダウンロード</md-button
              >
            </div>
          </div>
        </div>
      </Mt15>
    </div>
    <div class="flex flex-around">
      <div class="first-column">
        <h2 v-if="editMode">{{ showJpDate(selectedDate) }}の利用者数の編集</h2>
        <h2 v-else>{{ showJpDate(selectedDate) }}の利用者</h2>
        <table class="daily-report">
          <thead>
            <tr>
              <th rowspan="2">運転者名</th>
              <th rowspan="2">車両番号</th>
              <th rowspan="2">開始km</th>
              <th rowspan="2">終了㎞</th>
              <th rowspan="2">コース名</th>
              <th rowspan="2">路線名</th>
              <th rowspan="2">便数</th>
              <th rowspan="2">停留所</th>
              <th colspan="4">現金</th>
              <th colspan="3">回数券</th>
              <th rowspan="2">定期</th>
              <th rowspan="2">無料</th>
              <th rowspan="2">降車</th>
              <th v-if="!editMode" rowspan="2">計</th>
            </tr>
            <tr>
              <th>大人</th>
              <th>小人</th>
              <th>障害者大</th>
              <th>障害者小</th>
              <th>大人</th>
              <th>小人</th>
              <th>障害者</th>
            </tr>
          </thead>
          <tbody v-if="editMode">
            <tr
              v-for="(item, index) in FilteredDailyReport"
              :key="`first-${index}`"
            >
              <td>{{ item.driver_name }}</td>
              <td>{{ item.bus_number }}</td>
              <td>{{ item.mileage_start }}</td>
              <td>{{ item.mileage_end }}</td>
              <td>{{ item.course_name }}</td>
              <td>{{ item.route_name }}</td>
              <td>{{ item.route_order__order }}</td>
              <td>{{ item.bus_stop_name }}</td>
              <td><input v-model="item.cash_adult.number" /></td>
              <td><input v-model="item.cash_child.number" /></td>
              <td><input v-model="item.cash_handicapped_adult.number" /></td>
              <td><input v-model="item.cash_handicapped_child.number" /></td>
              <td><input v-model="item.coupon_adult.number" /></td>
              <td><input v-model="item.coupon_child.number" /></td>
              <td><input v-model="item.coupon_handicapped.number" /></td>
              <td><input v-model="item.commuter_pass.number" /></td>
              <td><input v-model="item.free.number" /></td>
              <td><input v-model="item.get_off.number" /></td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr v-for="(item, index) in FilteredDailyReport" :key="index">
              <td>{{ item.driver_name }}</td>
              <td>{{ item.bus_number }}</td>
              <td>{{ item.mileage_start }}</td>
              <td>{{ item.mileage_end }}</td>
              <td>{{ item.course_name }}</td>
              <td>{{ item.route_name }}</td>
              <td>{{ item.route_order__order }}</td>
              <td>{{ item.bus_stop_name }}</td>
              <td>{{ item.cash_adult.number }}</td>
              <td>{{ item.cash_child.number }}</td>
              <td>{{ item.cash_handicapped_adult.number }}</td>
              <td>{{ item.cash_handicapped_child.number }}</td>
              <td>{{ item.coupon_adult.number }}</td>
              <td>{{ item.coupon_child.number }}</td>
              <td>{{ item.coupon_handicapped.number }}</td>
              <td>{{ item.commuter_pass.number }}</td>
              <td>{{ item.free.number }}</td>
              <td>{{ item.get_off.number }}</td>
              <td>{{ item.sum }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- ダウンロード用モーダル -->
    <div id="download-modal" v-show="showContent" @click="hideDownloadModal">
      <div id="download-overlay" @click="hideDownloadModal">
        <div id="download-modal-content" @click="stopEvent">
          <p>ダウンロードする日報の年月を選択してください</p>
          <datepicker
            :inline="true"
            :maximum-view="'year'"
            :minimum-view="'month'"
            :initial-view="'month'"
            :language="ja"
            :open-date="downloadDate"
            v-model="downloadDate"
          ></datepicker>
          <div id="download-modal-button">
            <md-button @click="hideDownloadModal">取り消し</md-button>
            <md-button
              class="md-warning"
              @click="downloadCSV(), hideDownloadModal()"
              >ダウンロード開始</md-button
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Datepicker from "vuejs-datepicker";
import { ja } from "vuejs-datepicker/dist/locale";
// import moment from "moment";
export default {
  components: {
    Datepicker,
  },
  name: "DailyReport",
  data() {
    const today = new Date();
    const todayString = today.toISOString().slice(0, 10);
    return {
      dailyReportApiUrl: "/web/report/day/",
      dailyReportEditApiUrl: "/web/report/day/update/",
      courseListApiUrl: "/bus/course/",
      editMode: false,
      selectedDate: todayString,
      downloadDate: today,
      adultPrice: 100,
      childPrice: 50,
      handicappedPrice: 50,
      dailyReport: [],
      original_reports: [],
      selectedCourse: null,
      courses: [],
      ja: ja,
      showContent: false,
    };
  },
  methods: {
    /**
     * データの更新
     */
    async setReportData() {
      const params = {
        date: this.selectedDate,
      };
      let result = await this.callPostAPI(this.dailyReportApiUrl, params);
      this.courses = result.courses;
      this.selectedCourse = this.courses[0];
      this.dailyReport = result.dailyReport;
      this.original_reports = JSON.parse(JSON.stringify(this.dailyReport));
    },
    /**
     * csvのダウンロード
     */
    async downloadCSV() {
      this.notifyPanel(
        "<p>日報のダウンロードを開始します.</p>",
        "info",
        "top",
        "left"
      );
      axios
        .post(
          this.baseUrl + "/web/report/day/download/",
          this.downloadParameters,
          {
            responseType: "arraybuffer",
            headers: {
              Authorization: `Bearer ${this.$store.state.token}`,
              "Content-Type": "application/json",
            },
          }
        )
        .then((response) => {
          let fileURL = window.URL.createObjectURL(
            new Blob([response.data], {
              type: "application/zip",
              endings: "native",
            })
          );
          let fileLink = document.createElement("a");
          fileLink.href = fileURL;
          fileLink.download =
            `宇和島市三間地区コミュニティバス日報` +
            "_" +
            this.downloadParameters.year +
            "_" +
            this.downloadParameters.month;
          fileLink.click();
        })
        .catch(() => {
          this.notifyPanel(
            "<p>日報のダウンロードに失敗しました.</p>",
            "danger",
            "top",
            "left"
          );
        });
    },
    /**
     * データをアップロード
     */
    async updateReport() {
      const params = {
        course_id: this.selectedCourse,
        date: this.selectedDate,
        dailyReport: this.dailyReport,
      };
      console.log(params);
      var result = await this.callPostAPI(this.dailyReportEditApiUrl, params);
      this.notifyRegister(result.success);
      if (result.success === true) {
        this.setReportData();
      }
    },
    /**
     * 編集切り替え
     */
    changeEditMode() {
      this.editMode = !this.editMode;
    },
    /**
     * 編集キャンセル
     */
    cancelEdit() {
      console.log(this.dailyReport);
      console.log(this.original_reports);
      this.dailyReport = JSON.parse(JSON.stringify(this.original_reports));
    },
    /**
     * 日付を表示
     */
    showJpDate(theDate) {
      let date = theDate.split("-");
      return date[0] + "年" + date[1] + "月" + date[2] + "日";
    },
    /**
     * ダウンロード用のモーダルを表示
     */
    showDownloadModal() {
      this.showContent = true;
    },
    /**
     * ダウンロード用のモーダルを非表示
     */
    hideDownloadModal() {
      this.showContent = false;
    },
    stopEvent() {
      event.stopPropagation();
    },
  },
  created: function () {
    this.setReportData();
  },
  computed: {
    FilteredDailyReport: function () {
      return this.dailyReport.filter(
        (item) => item.course_name === this.selectedCourse
      );
    },
    downloadParameters: {
      get: function () {
        const date = this.downloadDate;
        return {
          year: date.getFullYear(),
          month: date.getMonth() + 1,
        };
      },
      set: function (date) {
        this.downloadDate = date;
      },
    },
  },
  watch: {
    selectedDate: function () {
      this.setReportData();
      let date = this.selectedDate.split("-");
      this.downloadDate = new Date(date[0], date[1] - 1, date[2]);
    },
    deep: true,
  },
};
</script>

<style lang="scss" scoped>
.download-button {
  height: 57px;
}
.flex {
  display: flex;
  .first-column {
    width: 80%;
    h2 {
      text-align: center;
    }
  }
}
.flex-around {
  justify-content: space-around;
}
.flex-between {
  justify-content: space-between;
}
.daily-report {
  border-spacing: 0;
  width: 100%;
  thead {
    display: table-header-group;
  }
  th {
    border: 1px solid #000000;
  }

  td {
    border: 1px solid #000000;
    text-align: center;

    input {
      width: 100%;
    }
  }
}
#download-overlay {
  z-index: 999;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.25);

  display: flex;
  align-items: flex-start;
  justify-content: center;
}
#download-modal-content {
  margin-top: 90pt;
  z-index: 1000;
  width: 50%;
  padding: 1em;
  background: #fff;
}
#download-modal-content {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
}
#download-modal-button {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-around;
}
</style>
