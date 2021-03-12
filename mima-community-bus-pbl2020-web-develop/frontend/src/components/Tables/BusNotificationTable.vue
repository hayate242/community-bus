<template>
  <div>
    <md-table v-model="histories" :table-header-color="tableHeaderColor">
      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="日付">{{ item.date }}</md-table-cell>
        <md-table-cell md-label="時刻">{{ item.time }}</md-table-cell>
        <md-table-cell md-label="バス名">{{ item.bus_name }}</md-table-cell>
        <md-table-cell md-label="コース名">{{
          item.course_name
        }}</md-table-cell>
        <md-table-cell md-label="内容">{{ item.content }}</md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>

<script>
export default {
  name: "bus-notification-table",
  props: {
    tableHeaderColor: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      serviceHistoryApiUrl: "/web/service/notification/history/",
      selected: [],
      histories: [],
    };
  },
  methods: {
    async setData() {
      // バス運行履歴取得
      var params = {
        limit: "5",
      };
      const history = await this.callPostAPI(this.serviceHistoryApiUrl, params);
      this.$set(this, "histories", history.histories);
    },
  },
  mounted: function () {
    this.setData();
  },
};
</script>
