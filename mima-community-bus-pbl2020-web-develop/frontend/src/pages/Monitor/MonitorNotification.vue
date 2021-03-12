<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item">
        <md-card>
          <div v-if="edit == null">
            <md-card-header data-background-color="green">
              <h4 class="title">見守り通知メッセージ</h4>
            </md-card-header>
            <md-card-content>
              <div class="md-layout-item md-size-100">
                <div class="places-buttons text-center">
                  <div class="md-layout">
                    {{ message.message }}
                  </div>
                </div>
              </div>
            </md-card-content>
          </div>

          <div v-else>
            <md-card-header data-background-color="blue">
              <h4 class="title">見守り通知メッセージ</h4>
            </md-card-header>
            <md-card-content>
              <div class="md-layout-item md-size-100">
                <div class="places-buttons text-center">
                  <div class="md-layout">
                    <md-field>
                      <md-textarea v-model="message.message">
                        {{ message.message }}
                      </md-textarea>
                    </md-field>
                  </div>
                </div>
              </div>
            </md-card-content>
          </div>
        </md-card>

        <div v-if="edit == null">
          <md-button class="md-info" @click="editFlg()">
            通知メッセージの変更
          </md-button>
        </div>

        <div v-else>
          <md-button class="md-warning" @click="editFlg(), updateMessage()">
            通知メッセージの変更確定
          </md-button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  name: "MonitorNotification",
  data() {
    return {
      edit: null,
      message: {
        message: null,
      },
    };
  },
  methods: {
    /**
     * 編集画面の出力スイッチ
     */
    editFlg() {
      if (this.edit == null) {
        this.edit = "edit";
      } else {
        this.edit = null;
      }
    },

    /**
     * 変更確定時の処理
     */
    async updateMessage() {
      let url = "/web/monitor/notification/update/";

      const data = {
        message: this.message.message,
      };
      let result = await this.callPostAPI(url, data);

      url = "/web/monitor/notification/";
      this.message = await this.callGetAPI(url, "");

      this.notifyUpdate(result.success);
    },
  },
  async mounted() {
    let url = "/web/monitor/notification/";
    this.message = await this.callGetAPI(url, "");
  },
};
</script>
<style></style>
