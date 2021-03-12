import axios from "axios";
import store from "../store";
export default {
  data() {
    return {
      baseUrl: process.env.VUE_APP_API_BASE_URL
    };
  },
  methods: {
    /**
     * GETでAPIを叩く関数
     * @param  {String}  url    エンドポイントのURL
     * @param  {Object}  params requestに入れるデータ
     * @return {Object}         response
     */
    async callGetAPI(url, params, require_auth = true) {
      var payload = {};
      var result = true;
      if (require_auth) {
        payload = {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
            "Content-Type": "application/json"
          },
          params
        };
      } else {
        payload = {
          headers: {
            "Content-Type": "application/json"
          },
          params
        };
      }
      const response = await axios
        .get(this.baseUrl + url, payload)
        .catch((error) => {
          console.log("callGetAPI error");
          // トークンの有効期限切れの処理
          if (error.response) {
            if(error.response.status == 401){
              this.redirectLogout()
            }
          }
          result = false
        });
        return result? response.data: [];
    },
    /**
     * POSTでAPIを叩く関数
     * @param  {String}  url    エンドポイントのURL
     * @param  {Object}  params requestに入れるデータ
     * @return {Object}         response
     */
    async callPostAPI(url, params) {
      var result = true;
      const response = await axios
        .post(this.baseUrl + url, params, {
          headers: {
            Authorization: `Bearer ${this.$store.state.token}`,
            "Content-Type": "application/json"
          }
        })
        .catch(() => {
          console.log("callPostAPI error");
          // トークンの有効期限切れの処理
          if (error.response) {
            if(error.response.status == 401){
              this.redirectLogout()
            }
          }
          result = false
        });
      return result? response.data: [];
    }
  }
};