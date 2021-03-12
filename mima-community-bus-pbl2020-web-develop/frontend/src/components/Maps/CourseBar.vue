<template>
  <div class="mt-15">
    <div class="md-layout md-gutter md-alignment-center">
      <div
        class="md-layout-item md-medium-size-33 md-small-size-50 md-xsmall-size-100 route-color"
        v-for="route in routes"
        :key="route.id"
      >
        <span :style="route.style">{{ route.route_name }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    routes: {
      type: Array,
      required: true,
      default: () => []
    }
  }
};
</script>
