<template>
<div class="wrapper" :class="{ 'nav-open': $sidebar.showSidebar }">
  <notifications></notifications>

  <side-bar :sidebar-item-color="sidebarBackground" :sidebar-background-image="sidebarBackgroundImage">

    <sidebar-link to="/admin/dashboard">
      <md-icon>dashboard</md-icon>
      <p>トップ</p>
    </sidebar-link>

    <div v-if="this.$store.state.group == '宇和島市職員' ||
    this.$store.state.group == 'ICTコース' ||
    this.$store.state.group == '委託バス会社職員'
    ">
      <sidebar-link to="/admin/report">
        <md-icon>library_books</md-icon>
        <p>日報</p>
      </sidebar-link>
    </div>

    <div v-if="this.$store.state.group == '宇和島市職員' ||
    this.$store.state.group == 'ICTコース' ||
    this.$store.state.group == '委託バス会社職員'
    ">
      <sidebar-link to="/admin/bus_record">
        <md-icon>content_paste</md-icon>
        <p>運行記録確認</p>
      </sidebar-link>
    </div>


    <div v-if="this.$store.state.group == '宇和島市職員' ||
    this.$store.state.group == 'ICTコース'
    ">
      <sidebar-link to="/admin/notifications">
        <md-icon>notifications</md-icon>
        <p>お知らせ管理</p>
      </sidebar-link>
    </div>


    <div v-if="this.$store.state.group == '宇和島市職員' ||
    this.$store.state.group == 'ICTコース'
    ">
      <sidebar-link to="/admin/bus">
        <md-icon>location_on</md-icon>
        <p>バス路線管理</p>
      </sidebar-link>
    </div>


    <div v-if="this.$store.state.group == '宇和島市職員' ||
    this.$store.state.group == 'ICTコース' ||
    this.$store.state.group == '委託バス会社職員'
    ">
      <sidebar-link to="/admin/driver">
        <md-icon>directions_bus</md-icon>
        <p>運転手・車両管理</p>
      </sidebar-link>
    </div>

    <div v-if="this.$store.state.group == '宇和島市職員' ||
    this.$store.state.group == 'ICTコース'
    ">
      <sidebar-link to="/admin/monitor">
        <md-icon>person</md-icon>
        <p>見守り管理</p>
      </sidebar-link>
    </div>

    <div v-if="this.$store.state.group == '宇和島市職員' ||
    this.$store.state.group == 'ICTコース'
    ">
      <sidebar-link to="/admin/user">
        <md-icon>desktop_mac</md-icon>
        <p>システムユーザー管理</p>
      </sidebar-link>
    </div>

    <div v-if="this.$store.state.group == '宇和島市職員' ||
    this.$store.state.group == 'ICTコース'
    ">
      <sidebar-link to="/admin/fare">
        <!-- <md-icon>cloud_download</md-icon> -->
        <md-icon>
          <font-awesome-icon :icon="['fas', 'yen-sign']" :style="{ color: 'white' }" />
        </md-icon>
        <p>運賃管理</p>
      </sidebar-link>
    </div>

    <div v-if="this.$store.state.group == '宇和島市職員' ||
    this.$store.state.group == 'ICTコース'
    ">
      <sidebar-link to="/admin/downloads">
        <md-icon>cloud_download</md-icon>
        <p>システムのダウンロード</p>
      </sidebar-link>
    </div>

  </side-bar>

  <div class="main-panel">
    <top-navbar></top-navbar>

    <dashboard-content> </dashboard-content>

    <content-footer v-if="!$route.meta.hideFooter"></content-footer>
  </div>
</div>
</template>

<script>
import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./Content.vue";
import { library } from '@fortawesome/fontawesome-svg-core'
import { faYenSign } from '@fortawesome/free-solid-svg-icons'

library.add(faYenSign)

export default {
  components: {
    TopNavbar,
    DashboardContent,
    ContentFooter
  },
  data() {
    return {
      sidebarBackground: "green",
      sidebarBackgroundImage: require("@/assets/img/sidebar-2.jpg")
    };
  }
};
</script>
