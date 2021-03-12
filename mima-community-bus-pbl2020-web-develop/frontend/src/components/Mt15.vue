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
  margin-top: 15px;
}
</style>
