import axios from "axios";
import store from "./../store.js";

export default {
  methods: {
    /**
     * ページの最下部へ移動する関数
     */
    goToEdit() {
      document.getElementById("edit").scrollIntoView(true)
    },

  }
};
