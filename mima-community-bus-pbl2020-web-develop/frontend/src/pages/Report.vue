<template>
<div class="content">
  <div class="md-layout">
    <div class="md-layout-item">
      <div class="md-layout-item md-medium-size-100 md-size-100">
        <div class="md-layout-item md-medium-size-100 md-xsmall-size-100 md-size-100">
          <nav-tabs-card>
            <template slot="content">
              <span class="md-nav-tabs-title"></span>
              <md-tabs class="md-success" md-alignment="left">
                <md-tab id="tab-daily-report" md-label="日報の編集とダウンロード" md-icon="poll" to="#daily-report">
                  <daily-report class="height-fix"></daily-report>
                </md-tab>

                <md-tab id="tab-monthly-report" md-label="月報のダウンロード" md-icon="poll" to="#monthly-report">
                  <monthly-report class="height-fix"></monthly-report>
                </md-tab>
              </md-tabs>
            </template>
          </nav-tabs-card>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import {
  NavTabsCard,
  DailyReport,
  MonthlyReport
} from "@/components";

export default {
  components: {
    NavTabsCard,
    DailyReport,
    MonthlyReport
  }
};
</script>
<style>
.height-fix {
  min-height: 500px;
}
</style>
