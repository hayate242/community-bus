// =========================================================
// * Vue Material Dashboard - v1.4.0
// =========================================================
//
// * Product Page: https://www.creative-tim.com/product/vue-material-dashboard
// * Copyright 2019 Creative Tim (https://www.creative-tim.com)
// * Licensed under MIT (https://github.com/creativetimofficial/vue-material-dashboard/blob/master/LICENSE.md)
//
// * Coded by Creative Tim
//
// =========================================================
//
// * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import Vuex from "vuex";
import VueRouter from "vue-router";
import Vuelidate from "vuelidate";
import VueCtkDateTimePicker from "vue-ctk-date-time-picker";
import "vue-ctk-date-time-picker/dist/vue-ctk-date-time-picker.css";
import Mt15 from "./components/Mt15";
import Right from "./components/Right";
import App from "./App";
import NavTabsCard from "./components/Cards/NavTabsCard.vue";
import {
  MonthPicker
} from "vue-month-picker";
import {
  MonthPickerInput
} from "vue-month-picker";

import VuejsDialog from "vuejs-dialog";
import VuejsDialogMixin from "vuejs-dialog/dist/vuejs-dialog-mixin.min.js";
import "vuejs-dialog/dist/vuejs-dialog.min.css";
import now from "./utils/now";
import APIfunction from "./utils/APIfunction";
import goToEdit from "./utils/goToEdit";
import Notify from "./utils/notify";
import login from "./utils/login";
import draggable from "vuedraggable";
import VModal from "vue-js-modal";
import store from "./store.js";

// router setup
import routes from "./routes/routes";

// Plugins
import GlobalComponents from "./globalComponents";
import GlobalDirectives from "./globalDirectives";
import Notifications from "./components/NotificationPlugin";

// MaterialDashboard plugin
import MaterialDashboard from "./material-dashboard";

import Chartist from "chartist";

// configure router
const router = new VueRouter({
  mode: "history",
  routes, // short for routes: routes
  linkExactActiveClass: "nav-item active"
});

// fontawesome
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

//ルーティング制御
router.beforeEach((to, from, next) => {
  if (to.path == "/") {
    //利用者トップへ遷移
    next();
  } else if (store.state.token == null && to.path != "/login") {
    //ログイン画面へ遷移
    next("/login");
  } else {
    //ログイン済みなら通常の遷移
    next();
  }
});

Vue.prototype.$Chartist = Chartist;

Vue.use(VueRouter);
Vue.use(MaterialDashboard);
Vue.use(GlobalComponents);
Vue.use(GlobalDirectives);
Vue.use(Notifications);
Vue.use(Vuelidate);
Vue.use(MonthPicker);
Vue.use(MonthPickerInput);
Vue.use(VuejsDialog);
Vue.component("VueCtkDateTimePicker", VueCtkDateTimePicker);
Vue.component("NavTabsCard", NavTabsCard);
Vue.component("Mt15", Mt15);
Vue.component("Right", Right);
Vue.component("draggable", draggable);
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.mixin(now);
Vue.mixin(APIfunction);
Vue.mixin(goToEdit);
Vue.mixin(Notify);
Vue.mixin(login);
Vue.use(VModal);

/* eslint-disable no-new */
new Vue({
  el: "#app",
  render: h => h(App),
  router,
  store,
  data: {
    Chartist: Chartist
  },
  components: {
    Mt15,
    Right,
    NavTabsCard,
    draggable
  }
});