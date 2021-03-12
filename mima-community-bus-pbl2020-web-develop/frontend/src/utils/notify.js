export default {
  methods: {
    /**
     * 通知文の追加
     *
     * @param {*} message
     * @param {*} type
     * @param {*} verticalAlign
     * @param {*} horizontalAlign
     */
    notifyPanel(message, type, verticalAlign, horizontalAlign) {
      scrollTo(0, 0);
      this.$notify({
        message,
        icon: "add_alert",
        horizontalAlign: horizontalAlign,
        verticalAlign: verticalAlign,
        type
      });
    },
    /**
     * 登録成功時のメッセージ
     *
     * @param {*} isSuccess
     */
    notifyRegister(isSuccess, message = "") {
      if (isSuccess) {
        this.notifyPanel("<p>登録しました.</p>", "info", "top", "left");
      } else {
        if (message != "") {
          this.notifyPanel("<p>" + message + "</p>", "danger", "top", "left");
        } else {
          this.notifyPanel("<p>登録に失敗しました.</p>", "danger", "top", "left");
        }
      }
    },
    /**
     * 更新成功時のメッセージ
     *
     * @param {*} isSuccess
     */
    notifyUpdate(isSuccess, message = "") {
      if (isSuccess) {
        this.notifyPanel("<p>更新しました.</p>", "info", "top", "left");
      } else {
        if (message != "") {
          this.notifyPanel("<p>" + message + "</p>", "danger", "top", "left");
        } else {
          this.notifyPanel("<p>更新に失敗しました.</p>", "danger", "top", "left");
        }
      }
    },
    /**
     * 削除成功時のメッセージ
     *
     * @param {*} isSuccess
     */
    notifyDelete(isSuccess, message = "") {
      if (isSuccess) {
        this.notifyPanel("<p>削除しました.</p>", "info", "top", "left");
      } else {
        if (message != "") {
          this.notifyPanel("<p>" + message + "</p>", "danger", "top", "left");
        } else {
          this.notifyPanel("<p>削除に失敗しました.</p>", "danger", "top", "left");
        }
      }
    }
  }
};