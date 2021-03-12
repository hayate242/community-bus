<template>
<router-view></router-view>
</template>

<script>
export default {
  name: "ThemeColors",
  methods: {
    createPageTitle: function(to) {
      if (to.meta.title) {
        var setTitle = to.meta.title;
        document.title = setTitle;
      } else {
        document.title = "みまっぷ | 三間地区コミュニティバス運行管理システム"
      }
    }
  },
  mounted: function() {
    var to = this.$route;
    this.createPageTitle(to);
  },
  watch: {
    '$route'(to, from) {
      this.createPageTitle(to);
    }
  }
};
</script>
<style lang="scss">
@import "~vue-material/dist/theme/engine";

.mt-15 {
    margin-top: 15px;
}
</style>
