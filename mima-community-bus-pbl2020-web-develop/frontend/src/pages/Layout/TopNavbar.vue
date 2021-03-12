<template>
  <md-toolbar md-elevation="0" class="md-transparent">
    <div class="md-toolbar-row">
      <div class="md-toolbar-section-start">
        <h3 class="md-title">{{ $route.name }}</h3>
      </div>
      <div class="md-toolbar-section-end">
        <md-list>
          <md-list-item href="#/user">
            <i class="material-icons">person</i>
            <!-- <p class="hidden-lg hidden-md">Profile</p> -->
            <i>{{ userName }}</i>
          </md-list-item>
          <md-button class="md-danger" @click="logout">ログアウト</md-button>
        </md-list>
        <md-button
          class="md-just-icon md-simple md-toolbar-toggle"
          :class="{ toggled: $sidebar.showSidebar }"
          @click="toggleSidebar"
        >
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
          <span class="icon-bar"></span>
        </md-button>
      </div>
    </div>
  </md-toolbar>
</template>

<script>
import store from "./../../store.js";
export default {
  data() {
    return {};
  },
  methods: {
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    logout() {
      store.commit("logout");
      this.$router.push("/login");
    }
  },
  computed: {
    userName: function() {
      return store.state.userName;
    }
  }
};
</script>

<style lang="css"></style>
