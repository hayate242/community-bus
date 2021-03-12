<template>
<div class="content">
  <!-- contents -->
  <div class="md-layout">
    <!-- header -->
    <md-toolbar class="header-theme" md-elevation="1">
      <div class="flex-wrap">
        <h3>みまっぷ</h3>
        <h5 class="header-sub-title ml-15">
          〜三間地区コミュニティバス管理システム〜
        </h5>
      </div>
      <!-- Todo 見守り閲覧追加 -->
      <!-- <md-button>Refresh</md-button>
      <md-button class="md-primary">Create</md-button> -->
    </md-toolbar>
    <div class="md-layout-item sp">
      <current-notification-card :cardHeaderText="currentNotificationHeaderText" :message="items.message" />
      <!-- bus location -->
      <div class="md-layout-item md-medium-size-100 md-size-100">
        <bus-location-map></bus-location-map>
      </div>
      <!-- bus location -->
      <!-- bus運行状況 -->
      <md-card>
        <md-card-header data-background-color="green">
          <h4 class="title">現在の運行状況</h4>
        </md-card-header>
        <md-card-content>
          <bus-status-card :selectDate="selectDate" />
        </md-card-content>
      </md-card>
      <!-- bus運行状況 -->
      <content-footer></content-footer>
    </div>
  </div>
</div>
</template>

<script>
import ContentFooter from "./Layout/ContentFooter";
import {
  CurrentNotificationCard,
  BusLocationMap,
  BusStatusCard,
} from "@/components";
export default {
  components: {
    BusLocationMap,
    CurrentNotificationCard,
    BusStatusCard,
    ContentFooter,
  },
  data() {
    return {
      selectDate: false,
      currentNotificationHeaderText: "お知らせ",
      items: {},
      width: null,
      spFlg: false
    };
  },
  async mounted() {
    let url = "/web/notification/";
    this.items = await this.callGetAPI(url, "", false);
  },
};
</script>
<style>
.sp {
  max-width: 100%;
}
</style>
