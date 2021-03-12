<template>
  <div>
    <md-table
      v-model="systemNotifications"
      :table-header-color="tableHeaderColor"
    >
      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="日付">{{ item.date }}</md-table-cell>
        <md-table-cell md-label="時刻">{{ item.time }}</md-table-cell>
        <md-table-cell md-label="内容">{{ item.content }}</md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>

<script>
export default {
  name: "system-notification-table",
  props: {
    tableHeaderColor: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      systemNotificationApiUrl: "/web/system/notification/history/",
      selected: [],
      systemNotifications: [],
    };
  },
  methods: {
    async setData() {
      // システム変更履歴取得
      var params = {
        limit: "5",
      };
      const history = await this.callPostAPI(
        this.systemNotificationApiUrl,
        params
      );
      this.$set(this, "systemNotifications", history.histories);
    },
  },
  mounted: function () {
    this.setData();
  },
};
</script>
