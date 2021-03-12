import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    userId: null,
    userName: null,
    token: null,
    group: null,
    path_data: [],
    route_locations: [],
  },
  plugins: [createPersistedState()],
  mutations: {
    /**
     * ログイン時にユーザーid，ユーザー名，トークンを格納する関数
     */
    login(state, payload) {
      state.token = payload.token;
      state.userId = payload.userId;
      state.userName = payload.userName;
      state.group = payload.group;
    },

    /**
     *  ログアウト時にユーザーid，ユーザー名，トークンを格破棄する関数
     */
    logout(state) {
      state.token = null;
      state.userId = null;
      state.userName = null;
      state.group = null;
    },

    /**
     * 経路情報の保存
     */
    path(state, payload) {
      state.route_locations = payload.route_locations;
      state.path_data.push(payload.path_data);
    },

    /**
     * path_dataとroute_locationsをクリアする関数
     */
    path_clear(state) {
      state.route_locations = [];
      state.path_data = [];
    }
  },
  getters: {
    group: state => (state.group ? state.group : ""),
    token: state => (state.token ? state.token : ""),
    path_data: state => (state.path_data ? state.path_data : ""),
    route_locations: state => (state.route_locations ? state.route_locations : "")
  }
});

export default store;