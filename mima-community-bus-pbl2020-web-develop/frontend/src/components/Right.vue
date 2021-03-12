<template>
  <div class="content">
    <slot></slot>
  </div>
</template>
<script>
export default {
  props: {
    top: {
      type: Boolean,
      default: true
    }
  }
};
</script>
<style lang="scss" scoped>
.content {
  text-align: right;
  margin: 0 0 0 auto;
}
</style>
