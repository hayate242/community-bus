<template>
<div>
  <div class="md-layout">
    <VueCtkDateTimePicker id="startDate" class="md-layout-item" v-model="startDate" label="検索範囲を選択してください" format="YYYY-MM-DD" formatted="YYYY-MM-DD" overlay only-date noClearButton />
    <h4 class="md-layout-item center">から</h4>
    <VueCtkDateTimePicker id="endDate" class="md-layout-item" v-model="endDate" label="検索範囲を選択してください" :min-date="startDate" format="YYYY-MM-DD" formatted="YYYY-MM-DD" overlay only-date noClearButton />
  </div>
  <md-field>
    <label>見守り機能利用者選択</label>
    <md-select v-model="selectedUser">
      <md-option value="{all}">絞り込みなし</md-option>
      <md-option v-for="user in users.monitor_user" :key="user.card_id" :value="user.monitor_target_user_name">
        {{ user.monitor_target_user_name }}
      </md-option>
    </md-select>
  </md-field>

  <md-card>
    <md-card-header data-background-color="green">
      <h4 class="title">見守り機能利用履歴</h4>
    </md-card-header>
    <md-card-content>
      <div class="md-layout-item md-size-100">
        <md-table v-model="items">
          <md-table-row>
            <md-table-head>ユーザー名</md-table-head>
            <md-table-head>日付</md-table-head>
            <md-table-head>時刻</md-table-head>
            <md-table-head>バス停名</md-table-head>
          </md-table-row>

          <md-table-row v-for="item in items.history" :key="item.id">
            <md-table-cell>{{ item.name }}</md-table-cell>
            <md-table-cell>{{ item.date }}</md-table-cell>
            <md-table-cell>{{ item.time }}</md-table-cell>
            <md-table-cell>{{ item.bus_stop }}</md-table-cell>
          </md-table-row>
        </md-table>
      </div>
    </md-card-content>
  </md-card>
</div>
</template>
<script>
export default {
  name: "MonitorHistory",
  data() {
    return {
      selectedUser: "{all}",
      startDate: this.oneMonthsAgoDate(),
      endDate: this.nowDate(),
      users: [],
      items: [],
    };
  },
  watch: {
    /**
     * startDateのデータを監視して，変更があればendDateをnullにする
     * endDateが変更されるので，endDateの監視用関数が発火する．
     */
    startDate: function() {
      //endDateをnullにする
      //endDateが変更されるので，APIも叩かれる
      this.endDate = this.nowDate();
    },

    /**
     * endDataのデータを監視して，変更があればAPIを叩いて履歴表を更新する
     */
    endDate: async function() {
      let url = "/web/monitor/history/";

      //選択ユーザーをAPIに送信できる形に変更
      let userParam = "";
      if (this.selectedUser == "{all}") {
        userParam = "";
      } else {
        userParam = this.selectedUser;
      }

      let params = {
        start_date: this.startDate,
        end_date: this.endDate,
        selected_user: userParam,
      };
      this.items = await this.callPostAPI(url, params);
    },

    /**
     * selectedUserを監視して，変更があればAPIを叩いて履歴表を更新する
     */
    selectedUser: async function() {
      let url = "/web/monitor/history/";

      //選択ユーザーをAPIに送信できる形に変更
      let userParam = "";
      if (this.selectedUser == "{all}") {
        userParam = "";
      } else {
        userParam = this.selectedUser;
      }

      let params = {
        start_date: this.startDate,
        end_date: this.endDate,
        selected_user: userParam,
      };
      this.items = await this.callPostAPI(url, params);
    },
  },
  async mounted() {
    let url = "/web/monitor/management/";
    this.users = await this.callGetAPI(url, "");

    url = "/web/monitor/history/";

    //選択ユーザーをAPIに送信できる形に変更
    let userParam = "";
    if (this.selectedUser == "{all}") {
      userParam = "";
    } else {
      userParam = this.selectedUser;
    }

    let params = {
      start_date: this.startDate,
      end_date: this.endDate,
      selected_user: userParam,
    };
    console.log(params);

    this.items = await this.callPostAPI(url, params);
  },
};
</script>
<style>
.center {
  text-align: center;
}
</style>
