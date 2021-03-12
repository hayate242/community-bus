<template>
  <div class="md-layout-item md-medium-size-100 md-size-100">
    <md-card>
      <md-card-header data-background-color="green">
        <h4 class="title">{{ cardHeaderText }}</h4>
      </md-card-header>
      <md-card-content>
        <div class="md-layout-item md-size-100">
          <div class="places-buttons text-center">
            <div class="md-layout">
              {{ message }}
            </div>
          </div>
        </div>
      </md-card-content>
    </md-card>
  </div>
</template>

<script>
export default {
  props: {
    cardHeaderText: {
      type: String,
      required: true,
      default: "お知らせ"
    },
    message: {
      type: String,
      required: true,
      default: "メッセージ取得エラー"
    }
  },
  name: "current-notification-card"
};
</script>
