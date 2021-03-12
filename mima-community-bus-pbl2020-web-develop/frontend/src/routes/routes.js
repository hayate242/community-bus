import DashboardLayout from "@/pages/Layout/DashboardLayout.vue";
import multiguard from "vue-router-multiguard";

import Dashboard from "@/pages/Dashboard.vue";
import Report from "@/pages/Report.vue";
import UserProfile from "@/pages/UserProfile.vue";
import TableList from "@/pages/TableList.vue";
import Typography from "@/pages/Typography.vue";
import Icons from "@/pages/Icons.vue";
import Index from "@/pages/Index.vue";
import Notification from "@/pages/Notification";
import Monitor from "@/pages/Monitor/Monitor.vue";
import BusRecord from "@/pages/BusRecord.vue";
import DriverManagement from "@/pages/DriverManagement/DriverManagement.vue";
import UserManagement from "@/pages/UserManagement/UserManagement.vue";
import BusRoute from "@/pages/BusRoute/BusRoute.vue";
import Login from "@/pages/Login.vue";
import Fare from "@/pages/Fare/Fare.vue";
import Downloads from "@/pages/Downloads.vue";
import store from "./../store.js";

const tokenGuard = (to, from, next) => {
  if (store.getters["token"] != null) {
    next()
  } else {
    store.commit("logout")
    next("/login")
  }
}

const uwajimaGuard = (to, from, next) => {
  if (store.getters["group"] == "ICTコース" ||
    store.getters["group"] == "宇和島市職員") {
    next()
  } else {
    store.commit("logout")
    next("/")
  }
}

const busCompanyGuard = (to, from, next) => {
  if (store.getters["group"] == "ICTコース" ||
    store.getters["group"] == "宇和島市職員" ||
    store.getters["group"] == "委託バス会社職員") {
    next()
  } else {
    store.commit("logout")
    next("/")
  }
}

const routes = [{
    path: "/",
    component: Index,
    meta: {
      title: process.env.VUE_APP_TITLE
    },
  },
  {
    name: "login",
    path: "/login",
    component: Login,
    props: true,
    meta: {
      title: process.env.VUE_APP_LOGIN_TITLE
    },
  },
  {
    path: "/admin",
    component: DashboardLayout,
    redirect: to => {
      return "/admin/dashboard";
    },
    meta: {
      title: process.env.VUE_APP_ADMIN_TITLE
    },
    children: [{
        path: "dashboard",
        name: "トップ",
        component: Dashboard,
        beforeEnter: multiguard([tokenGuard, busCompanyGuard]),
        meta: {
          title: process.env.VUE_APP_ADMIN_TITLE
        },
      },
      {
        path: "report",
        name: "日報の確認",
        component: Report,
        beforeEnter: multiguard([tokenGuard, busCompanyGuard]),
        meta: {
          title: process.env.VUE_APP_ADMIN_TITLE
        },
      },
      {
        path: "bus_record",
        name: "運行記録の確認",
        component: BusRecord,
        beforeEnter: multiguard([tokenGuard, busCompanyGuard]),
        meta: {
          title: process.env.VUE_APP_ADMIN_TITLE
        },
      },
      {
        path: "notifications",
        name: "お知らせ管理",
        component: Notification,
        beforeEnter: multiguard([tokenGuard, uwajimaGuard]),
        meta: {
          title: process.env.VUE_APP_ADMIN_TITLE
        },
      },
      {
        path: "bus",
        name: "バス路線管理",
        component: BusRoute,
        beforeEnter: multiguard([tokenGuard, uwajimaGuard]),
        meta: {
          title: process.env.VUE_APP_ADMIN_TITLE
        },
      },
      {
        path: "driver",
        name: "運転手・車両管理",
        component: DriverManagement,
        beforeEnter: multiguard([tokenGuard, busCompanyGuard]),
        meta: {
          title: process.env.VUE_APP_ADMIN_TITLE
        },
      },
      {
        path: "monitor",
        name: "見守り管理",
        component: Monitor,
        beforeEnter: multiguard([tokenGuard, uwajimaGuard]),
        meta: {
          title: process.env.VUE_APP_ADMIN_TITLE
        },
      },
      {
        path: "user",
        name: "システムユーザー管理",
        component: UserManagement,
        beforeEnter: multiguard([tokenGuard, uwajimaGuard]),
        meta: {
          title: process.env.VUE_APP_ADMIN_TITLE
        },
      },
      {
        path: "fare",
        name: "運賃設定",
        component: Fare,
        meta: {
          title: process.env.VUE_APP_ADMIN_TITLE
        },
      },
      {
        path: "downloads",
        name: "システムのダウンロードとインストール手順",
        component: Downloads,
        meta: {
          title: process.env.VUE_APP_ADMIN_TITLE
        },
      }
    ]
  }
];

export default routes;