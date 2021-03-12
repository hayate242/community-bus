<template>
  <div>
    <div class="select-area">
      <Mt15>
        <div
          class="flex flex-between md-layout-item md-medium-size-100 md-size-100"
        >
          <div>
            <p>月を選択してください</p>
            <p>選択中：{{ date.year }}年{{ date.month }}</p>
            <month-picker-input
              v-model="date"
              :months="[
                '1月',
                '2月',
                '3月',
                '4月',
                '5月',
                '6月',
                '7月',
                '8月',
                '9月',
                '10月',
                '11月',
                '12月',
              ]"
              :default-month="thisMonth"
            ></month-picker-input>
          </div>
          <md-button class="md-primary download-button" @click="downloadCSV"
            >ダウンロード</md-button
          >
        </div>
      </Mt15>
    </div>
    <div class="flex flex-around">
      <div class="first-column">
        <h2>利用実績</h2>
        <table class="daily-report">
          <thead>
            <tr>
              <th rowspan="2">日付</th>
              <th colspan="3">現金</th>
              <th colspan="3">回数券利用</th>
              <th colspan="3">回数券販売</th>
              <th rowspan="2">定期</th>
              <th rowspan="2">無料</th>
              <th rowspan="2">計</th>
              <th
                rowspan="2"
                v-for="course in reports.courses"
                :key="course.id"
              >
                {{ course.course_name + "走行距離" }}
              </th>
            </tr>
            <tr>
              <th>大人</th>
              <th>小人</th>
              <th>障害者</th>
              <th>大人</th>
              <th>小人</th>
              <th>障害者</th>
              <th>大人</th>
              <th>小人</th>
              <th>障害者</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="report in reports.monthly_number_of_users_report"
              :key="report.day"
            >
              <td>{{ report.day }}</td>
              <td>{{ report.cash_adult }}</td>
              <td>{{ report.cash_child }}</td>
              <td>{{ report.cash_handicapped }}</td>
              <td>{{ report.coupon_adult }}</td>
              <td>{{ report.coupon_child }}</td>
              <td>{{ report.coupon_handicapped }}</td>
              <td>{{ report.coupon_adult_sale }}</td>
              <td>{{ report.coupon_child_sale }}</td>
              <td>{{ report.coupon_handicapped_sale }}</td>
              <td>{{ report.commuter_pass }}</td>
              <td>{{ report.free }}</td>
              <td>{{ report.sum }}</td>
              <td v-for="course in reports.courses" :key="course.id">
                {{ report["mileage_" + course.id] }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="second-column">
        <h2>売上</h2>
        <table class="daily-report">
          <thead>
            <tr>
              <th colspan="3">現金</th>
              <th colspan="3">回数券販売</th>
              <th rowspan="2">計（現金）</th>
              <th rowspan="2">計（全体）</th>
            </tr>
            <tr>
              <th>大人</th>
              <th>小人</th>
              <th>障害者</th>
              <th>大人</th>
              <th>小人</th>
              <th>障害者</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="report in reports.monthly_sum_of_fare_report"
              :key="report.day"
            >
              <td>{{ report.cash_adult }}</td>
              <td>{{ report.cash_child }}</td>
              <td>{{ report.cash_handicapped }}</td>
              <td>{{ report.coupon_adult_sale }}</td>
              <td>{{ report.coupon_child_sale }}</td>
              <td>{{ report.coupon_handicapped_sale }}</td>
              <td>{{ report.cash_all }}</td>
              <td>{{ report.report_all }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { MonthPickerInput } from "vue-month-picker";

export default {
  components: {
    MonthPickerInput,
  },
  name: "MonthlyReport",
  data: () => ({
    monthlyReportApiUrl: "/web/report/month/",
    selectedMonth: null,
    reports: {
      monthly_number_of_users_report: [],
      monthly_sum_of_fare_report: [],
      courses: [],
    },
    prices: [],
    date: {
      from: null,
      to: null,
      month: null,
      year: null,
    },
    thisMonth: 1,
  }),
  methods: {
    /**
     * 利用実績のセット
     */
    async setReportData() {
      const params = {
        year: this.date.year,
        month: String(this.date.month).slice(0, -1),
      };
      this.callPostAPI(this.monthlyReportApiUrl, params).then(
        (result) => (this.reports = result ? result : null)
      );
    },
    setDate() {
      let today = new Date();
      this.date.month = today.getMonth() + 1 + "月";
      this.thisMonth = today.getMonth();
      this.date.year = today.getFullYear();
    },
    /**
     * csv のダウンロード
     */
    downloadCSV() {
      var csv =
        "\ufeff" +
        "日付,現金大人,現金子供,現金障害者,回数券大人,回数券子供,回数券障害者,回数券販売大人,回数券販売子供,回数券販売障害者,定期,無料,合計," +
        this.reports.courses
          .map((course) => course.course_name + "走行距離")
          .join() +
        ",,現金大人,現金子供,現金障害者,回数券販売大人,回数券販売子供,回数券販売障害者,計（現金）,計（全体）\n";
      const day_length = this.reports.monthly_number_of_users_report.length;
      for (var i = 0; i < day_length; i++) {
        csv += this.csvLine(
          this.reports.monthly_number_of_users_report[i],
          this.reports.monthly_sum_of_fare_report[i]
        );
      }
      let blob = new Blob([csv], {
        type: "text/csv",
      });
      let link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.download =
        "三間地区コミュニティバス月報" +
        this.date.year +
        "年" +
        String(this.date.month) +
        ".csv";
      link.click();
    },
    /**
     * 1行csvを返却
     */
    csvLine(report, price) {
      return (
        this.strWithDelimiter(report["day"]) +
        this.strWithDelimiter(report["cash_adult"]) +
        this.strWithDelimiter(report["cash_child"]) +
        this.strWithDelimiter(report["cash_handicapped"]) +
        this.strWithDelimiter(report["coupon_adult"]) +
        this.strWithDelimiter(report["coupon_child"]) +
        this.strWithDelimiter(report["coupon_handicapped"]) +
        this.strWithDelimiter(report["coupon_adult_sale"]) +
        this.strWithDelimiter(report["coupon_child_sale"]) +
        this.strWithDelimiter(report["coupon_handicapped_sale"]) +
        this.strWithDelimiter(report["commuter_pass"]) +
        this.strWithDelimiter(report["free"]) +
        this.strWithDelimiter(report["sum"]) +
        this.reports.courses
          .map((course) =>
            this.strWithDelimiter(report["mileage_" + course.id])
          )
          .join("") +
        this.strWithDelimiter() +
        this.strWithDelimiter(price["cash_adult"]) +
        this.strWithDelimiter(price["cash_child"]) +
        this.strWithDelimiter(price["cash_handicapped"]) +
        this.strWithDelimiter(price["coupon_adult_sale"]) +
        this.strWithDelimiter(price["coupon_child_sale"]) +
        this.strWithDelimiter(price["coupon_handicapped_sale"]) +
        this.strWithDelimiter(price["cash_all"]) +
        price["report_all"] +
        "\n"
      );
    },
    /**
     * csv delimiter 付きの文字列を返す
     */
    strWithDelimiter(str = "") {
      return str + ",";
    },
  },
  created() {
    this.setDate();
    this.setReportData();
  },
  watch: {
    date: {
      handler: function (val, oldVal) {
        this.setReportData();
      },
      deep: true,
    },
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
    width: 50%;
    h2 {
      text-align: center;
    }
  }
  .second-column {
    width: 40%;
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
  }
}
</style>
