<template>
  <div class="md-layout">
    <div class="md-layout-item md-size-100">
      <nav-tabs-card>
        <template slot="content">
          <md-tabs md-sync-route class="md-success" md-alignment="left">
            <md-tab id="driver" md-label="運転手管理" to="#driver">
              <Driver />
            </md-tab>

            <md-tab id="bus" md-label="車両管理" to="#bus">
              <Bus />
            </md-tab>
          </md-tabs>
        </template>
      </nav-tabs-card>
    </div>
  </div>
</template>

<script>
import Driver from "./Driver.vue";
import Bus from "./Bus.vue";

export default {
  components: {
    Driver,
    Bus
  }
};
</script>

<style></style>
