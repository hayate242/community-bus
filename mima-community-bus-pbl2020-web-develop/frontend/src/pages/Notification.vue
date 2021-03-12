<template>
  <div class="content">
    <div class="md-layout">
      <div class="md-layout-item">
        <current-notification-card
          :cardHeaderText="currentNotificationHeaderText"
          :message="items.message"
        />

        <!-- TODO 2期で開発する -->
        <!-- <md-card>
          <md-card-header data-background-color="green">
            <h4 class="title">お知らせスケジュール一覧</h4>
          </md-card-header>
          <md-card-content>
            <div class="md-layout-item md-size-100">
              <md-table v-model="items">
                <md-table-row>
                  <md-table-head>メッセージ</md-table-head>
                  <md-table-head>開始日</md-table-head>
                  <md-table-head>終了日</md-table-head>
                  <md-table-head>開始時刻</md-table-head>
                  <md-table-head>終了時刻</md-table-head>
                  <md-table-head>曜日</md-table-head>
                </md-table-row>

                <md-table-row v-for="item in items.schedule" :key="item.id">
                  <md-table-cell>{{ item.message }}</md-table-cell>
                  <md-table-cell>{{ item.start_date }}</md-table-cell>
                  <md-table-cell>{{ item.end_date }}</md-table-cell>
                  <md-table-cell>{{ item.start_time }}</md-table-cell>
                  <md-table-cell>{{ item.end_time }}</md-table-cell>
                  <md-table-cell>{{ item.week }}</md-table-cell>
                </md-table-row>
              </md-table>
            </div>
          </md-card-content>
        </md-card> -->

        <md-card>
          <md-card-header data-background-color="green">
            <h4 class="title">お知らせメッセージ変更</h4>
          </md-card-header>

          <md-card-content>
            <md-card>
              <md-card-header data-background-color="blue">
                <h4 class="subTitle">メッセージ</h4>
              </md-card-header>
              <md-card-content>
                <span
                  class="error"
                  v-if="$v.notification.$invalid && $v.notification.$dirty"
                  >必須項目です</span
                >
                <md-field>
                  <md-textarea
                    v-model="notification"
                    @blur="$v.notification.$touch()"
                  ></md-textarea>
                </md-field>
              </md-card-content>
            </md-card>

            <!-- TODO 2期で開発する -->
            <!-- <md-card>
              <md-card-header data-background-color="blue">
                <h4 class="subTitle">スケジュールの設定</h4>
              </md-card-header>
              <md-card-content>
                <Mt15>
                  <VueCtkDateTimePicker
                    v-model="startDate"
                    label="開始日"
                    :min-date="now"
                    format="YYYY-MM-DD"
                    formatted="YYYY-MM-DD"
                    position="top"
                    overlay
                    only-date
                  />
                  <div v-if="startDate != null">
                    <VueCtkDateTimePicker
                      v-model="endDate"
                      label="終了日"
                      :min-date="startDate"
                      format="YYYY-MM-DD"
                      formatted="YYYY-MM-DD"
                      position="top"
                      overlay
                      only-date
                    />
                  </div>
                  <div v-else>
                    <VueCtkDateTimePicker
                      v-model="endDate"
                      label="開始日を入力してください"
                      :min-date="startDate"
                      format="YYYY-MM-DD"
                      formatted="YYYY-MM-DD"
                      position="top"
                      overlay
                      only-date
                      disabled
                    />
                  </div>
                </Mt15>
                <Mt15>
                  <VueCtkDateTimePicker
                    v-model="startTime"
                    label="開始時刻"
                    :min-date="now"
                    format="HH:mm"
                    formatted="HH:mm"
                    position="top"
                    overlay
                    only-time
                  />
                  <VueCtkDateTimePicker
                    v-model="endTime"
                    label="終了時刻"
                    format="HH:mm"
                    formatted="HH:mm"
                    position="top"
                    overlay
                    only-time
                  />
                </Mt15>

                <Mt15>
                  <label>繰り返し</label><br />
                  <md-checkbox v-model="week[0]">日曜日</md-checkbox>
                  <md-checkbox v-model="week[1]">月曜日</md-checkbox>
                  <md-checkbox v-model="week[2]">火曜日</md-checkbox>
                  <md-checkbox v-model="week[3]">水曜日</md-checkbox>
                  <md-checkbox v-model="week[4]">木曜日</md-checkbox>
                  <md-checkbox v-model="week[5]">金曜日</md-checkbox>
                  <md-checkbox v-model="week[6]">土曜日</md-checkbox>
                </Mt15>
              </md-card-content>
            </md-card> -->
            <md-button
              class="md-warning"
              @click="add()"
              :disabled="$v.$invalid"
            >
              お知らせメッセージの更新
            </md-button>
          </md-card-content>
        </md-card>
      </div>
    </div>
  </div>
</template>

<script>
import { required } from "vuelidate/lib/validators";
import { CurrentNotificationCard } from "@/components";
export default {
  components: {
    CurrentNotificationCard,
  },
  data() {
    return {
      currentNotificationHeaderText: "現在表示中のメッセージ",
      notification: null,
      startDate: null,
      endDate: null,
      startTime: null,
      endTime: null,
      now: null,
      week: [false, false, false, false, false, false, false],
      selected: [],
      items: {},
    };
  },
  methods: {
    async add() {
      if (this.error == true) {
        this.errorSwitch();
      }

      let data = {
        notification: this.notification,
      };

      let url = "/web/notification/update/";

      let result = await this.callPostAPI(url, data);

      if (result.success == true) {
        url = "/web/notification/";
        this.items = await this.callGetAPI(url, "");
        this.notifyPanel(
          "<p>以下の内容で登録しました.</p>" +
            "<p>メッセージ:" +
            this.notification,
          // "</p>" +
          // "<p>開始日:" +
          // this.startDate +
          // "</p>" +
          // "<p>終了日:" +
          // this.endDate +
          // "</p>" +
          // "<p>開始時刻:" +
          // this.startTime +
          // "</p>" +
          // "<p>終了時刻:" +
          // this.endTime +
          // "</p>" +
          // "<p>繰り返し設定:" +
          // this.week +
          // "</p>"
          "info",
          "top",
          "left"
        );
        this.reset();
      } else {
        this.notifyPanel("<p>登録に失敗しました.</p>", "danger", "top", "left");
        this.reset();
      }
    },
    reset() {
      this.notification = null;
      this.startDate = null;
      this.startTime = null;
      this.endDate = null;
      this.endTime = null;
      this.week = [false, false, false, false, false, false, false];
    },
  },
  watch: {
    startDate: function () {
      this.endDate = null;
    },
    startTime: function () {
      this.endTime = null;
    },
  },
  mounted: function () {
    this.now = this.nowDateTime();
  },
  async mounted() {
    let url = "/web/notification/";
    this.items = await this.callGetAPI(url, "", false);
    console.log(this.items);
  },
  validations: {
    notification: {
      required,
    },
  },
};
</script>
<style>
.error {
  color: #8a0421;
  border-color: #dd0f3b;
  background-color: #ffd9d9;
}
</style>
