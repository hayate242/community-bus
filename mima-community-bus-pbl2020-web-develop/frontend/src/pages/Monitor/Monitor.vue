<template>
  <div class="md-layout">
    <div class="md-layout-item md-size-100">
      <nav-tabs-card>
        <template slot="content">
          <md-tabs md-sync-route class="md-success" md-alignment="left">
            <md-tab
              id="notification"
              md-label="通知内容編集"
              to="#notification"
            >
              <MonitorNotification />
            </md-tab>

            <md-tab
              id="managemant"
              md-label="カードとユーザーの管理"
              to="#management"
            >
              <MonitorManagement />
            </md-tab>

            <md-tab id="history" md-label="見守り履歴" to="#history">
              <MonitorHistory />
            </md-tab>
          </md-tabs>
        </template>
      </nav-tabs-card>
    </div>
  </div>
</template>

<script>
import MonitorNotification from "./MonitorNotification.vue";
import MonitorManagement from "./MonitorManagement.vue";
import MonitorHistory from "./MonitorHistory.vue";

export default {
  components: {
    MonitorNotification,
    MonitorManagement,
    MonitorHistory
  }
};
</script>

<style lang="scss">
#history {
  min-height: 600px;
}
</style>
