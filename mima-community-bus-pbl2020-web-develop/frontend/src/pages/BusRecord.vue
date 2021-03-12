<template>
  <div class="content">
    <md-card>
      <md-card-header data-background-color="green">
        <h4 class="title">運行記録確認</h4>
      </md-card-header>
      <md-card-content>
        <bus-status-card :selectDate="selectDate" />
      </md-card-content>
    </md-card>
  </div>
</template>
<script>
import { BusStatusCard } from "@/components";
export default {
  components: {
    BusStatusCard
  },
  data() {
    return {
      selectDate: true
    };
  }
};
</script>
<style></style>
