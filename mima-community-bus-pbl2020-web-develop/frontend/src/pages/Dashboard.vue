<template>
  <div class="content">
    <div class="md-layout">
      <!-- bus location -->
      <h3 class="md-layout-item md-size-100 adjust-margin">バスの現在位置</h3>
      <div class="md-layout-item md-medium-size-100 md-size-100">
        <bus-location-map :mapStyles="mapStyles"></bus-location-map>
      </div>
      <!-- bus location -->
      <!-- コース運行状況 -->
      <!-- bus運行状況 -->
      <div class="md-layout-item md-medium-size-100 md-size-100">
        <md-card>
          <md-card-header data-background-color="green">
            <h4 class="title">現在の運行状況</h4>
          </md-card-header>
          <md-card-content>
            <bus-status-card :selectDate="selectDate" />
          </md-card-content>
        </md-card>
      </div>
      <!-- bus運行状況 -->
      <!-- コース運行状況 -->

      <!-- Phase2で機能追加 -->
      <!-- 統計情報 -->
      <!-- <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <h3>今週の乗車数の推移</h3>
        <chart-card
          :chart-data="dailyUserChart.data"
          :chart-options="dailyUserChart.options"
          :chart-type="'Line'"
          data-background-color="green"
        >
          <template slot="content">
            <h4 class="title">乗車数の推移</h4>
            <p class="category">
              <span class="text-success"
                ><i class="fas fa-long-arrow-alt-up"></i> 55%
              </span>
              上昇（前日比）
            </p>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon>access_time</md-icon>
              最終更新 4分前
            </div>
          </template>
        </chart-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <h3>月別乗車数の推移</h3>
        <chart-card
          :chart-data="monthlyUserChart.data"
          :chart-options="monthlyUserChart.options"
          :chart-responsive-options="monthlyUserChart.responsiveOptions"
          :chart-type="'Bar'"
          data-background-color="green"
        >
          <template slot="content">
            <h4 class="title">月別乗車数の推移</h4>
            <p class="category">
              Last Campaign Performance
            </p>
          </template>

          <template slot="footer">
            <div class="stats">
              <md-icon>access_time</md-icon>
              最終更新 10分前
            </div>
          </template>
        </chart-card>
      </div> -->
      <!-- 統計情報 -->
      <!-- お知らせ -->
      <!-- <h3 class="md-layout-item md-size-100">システム通知</h3>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <md-card>
          <md-card-header data-background-color="green">
            <h4 class="title">運行履歴</h4>
            <p class="category"></p>
          </md-card-header>
          <md-card-content>
            <bus-notification-table
              table-header-color="green"
            ></bus-notification-table>
            <p><a href="#">もっと見る</a></p>
          </md-card-content>
        </md-card>
      </div>
      <div
        class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-50"
      >
        <md-card>
          <md-card-header data-background-color="orange">
            <h4 class="title">システム変更履歴</h4>
            <p class="category"></p>
          </md-card-header>
          <md-card-content>
            <system-notification-table
              table-header-color="orange"
            ></system-notification-table>
            <p><a href="#">もっと見る</a></p>
          </md-card-content>
        </md-card>
      </div> -->
      <!-- お知らせ -->
    </div>
  </div>
  <!-- お知らせ -->
</template>

<script>
import {
  // ChartCard,
  // SystemNotificationTable,
  // BusNotificationTable,
  BusLocationMap,
  BusStatusCard,
} from "@/components";

export default {
  components: {
    // ChartCard,
    // SystemNotificationTable,
    // BusNotificationTable,
    BusLocationMap,
    BusStatusCard,
  },
  data() {
    return {
      selectDate: false,
      statisticsRidesApiUrl: "/statistics/rids/",
      mapStyles: {
        "max-height": "400px",
      },
      dailyUserChart: {
        data: {
          labels: [],
          series: [],
        },
        options: {
          lineSmooth: this.$Chartist.Interpolation.cardinal({
            tension: 0,
          }),
          low: 0,
          high: 50, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
          chartPadding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0,
          },
        },
      },
      dataCompletedTasksChart: {
        data: {
          labels: ["12am", "3pm", "6pm", "9pm", "12pm", "3am", "6am", "9am"],
          series: [[230, 750, 450, 300, 280, 240, 200, 190]],
        },
        options: {
          lineSmooth: this.$Chartist.Interpolation.cardinal({
            tension: 0,
          }),
          low: 0,
          high: 1000, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
          chartPadding: {
            top: 0,
            right: 0,
            bottom: 0,
            left: 0,
          },
        },
      },
      monthlyUserChart: {
        data: {
          labels: [],
          series: [],
        },
        options: {
          axisX: {
            showGrid: false,
          },
          low: 0,
          high: 100,
          chartPadding: {
            top: 0,
            right: 5,
            bottom: 0,
            left: 0,
          },
        },
        responsiveOptions: [
          [
            "screen and (max-width: 640px)",
            {
              seriesBarDistance: 5,
              axisX: {
                labelInterpolationFnc: function (value) {
                  return value[0];
                },
              },
            },
          ],
        ],
      },
    };
  },
  methods: {
    async setStatisticData() {
      // todo Phase2で機能追加
      // // 日別乗降者数チャート
      // var params = {
      //   option: "daily"
      // };
      // const dailyUserData = await this.callGetAPI(
      //   this.statisticsRidesApiUrl,
      //   params
      // );
      // this.$set(this.dailyUserChart, "data", dailyUserData);
      // // 月別乗降者数チャート
      // params = {
      //   option: "monthly"
      // };
      // const monthlyUserData = await this.callGetAPI(
      //   this.statisticsRidesApiUrl,
      //   params
      // );
      // this.$set(this.monthlyUserChart, "data", monthlyUserData);
    },
  },
  mounted: function () {
    this.setStatisticData();
  },
};
</script>
<style lang="scss">
.adjust-margin {
  margin-top: -36px;
}
</style>
