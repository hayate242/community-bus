import axios from "axios";
import store from "./../store.js";

export default {
  methods: {
    /**
     * ログイン用のAPIを叩き，tokenにベアラートークンを格納する
     * @param  {[type]}  email
     * @param  {[type]}  pass
     * @return {Object}       ユーザーid，ユーザー名，ベアラートークン
     */
    async login(email, pass) {
      const response = await axios
        .post(this.baseUrl + "/login/", {
          email: email + "",
          password: pass + ""
        })
        .catch(() => {
          console.log("login error");
        });

      if (
        response != null &&
        "data" in response &&
        "access_token" in response.data &&
        "user_id" in response.data &&
        "user_name" in response.data &&
        "group" in response.data
      ) {
        await store.commit({
          type: "login",
          token: response.data.access_token,
          userId: response.data.user_id,
          userName: response.data.user_name,
          group: response.data.group
        });
        return true;
      } else {
        return false;
      }
    },

    logout() {
      store.commit("logout");
    },
    redirectLogout(){
      this.logout()
      this.$router.push({name: "login", params: {message: "セッションの有効期限が切れました．<br>再度ログインしてください．"}});
    }
  }
};