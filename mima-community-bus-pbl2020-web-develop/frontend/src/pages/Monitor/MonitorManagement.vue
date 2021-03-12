<template>
<div>
  <Right v-if="show == false">
    <md-button class="md-info md-layout-item md-size-20" @click="newUserSwitch()">新規ユーザー登録</md-button>
  </Right>
  <div v-if="this.show == true">
    <md-card>
      <md-card-header data-background-color="blue">
        <h4 class="title">新規ユーザー登録</h4>
      </md-card-header>
      <md-card-content>
        <span class="error" v-if="$v.monitorUserName.$invalid && $v.monitorUserName.$dirty">必須項目です</span>
        <md-field>
          <label>保護者名</label>
          <md-input v-model="monitorUserName" @blur="$v.monitorUserName.$touch()"></md-input>
        </md-field>

        <span class="error" v-if="!$v.email.email && $v.email.$dirty">正しいメールアドレスを入力してください</span>
        <md-field>
          <label>メールアドレス</label>
          <md-input v-model="email" @blur="$v.email.$touch()"></md-input>
        </md-field>

        <span class="error" v-if="
              $v.monitorTargetUserName.$invalid &&
              $v.monitorTargetUserName.$dirty
            ">必須項目です</span>
        <md-field>
          <label>見守り対象名</label>
          <md-input v-model="monitorTargetUserName" @blur="$v.monitorTargetUserName.$touch()"></md-input>
        </md-field>

        <span class="error" v-if="!$v.cardNumber.required && $v.cardNumber.$dirty">必須項目です</span>
        <span class="error" v-if="
              (!$v.cardNumber.alphaNum ||
                !$v.cardNumber.minLength ||
                !$v.cardNumber.maxLength) &&
              $v.cardNumber.$dirty
            ">英数字16桁で入力してください</span>
        <md-field>
          <label>カード番号</label>
          <md-input v-model="cardNumber" @blur="$v.cardNumber.$touch()"></md-input>
        </md-field>
        <Right>
          <md-button class="md-size-20" @click="newUserSwitch(), reset()">登録取り消し</md-button>
          <md-button class="md-warning md-size-20" @click="newUserSwitch(), add(), reset()" :disabled="
                $v.monitorUserName.$invalid ||
                $v.cardNumber.$invalid ||
                $v.monitorTargetUserName.$invalid ||
                $v.email.$invalid
              ">登録確定</md-button>
        </Right>
      </md-card-content>
    </md-card>
  </div>

  <md-card>
    <md-card-header data-background-color="green">
      <h4 class="title">見守り機能利用者一覧</h4>
    </md-card-header>
    <md-card-content>
      <div class="md-layout-item md-size-100">
        <md-table v-model="items">
          <md-table-row>
            <md-table-head>保護者名</md-table-head>
            <md-table-head>メールアドレス</md-table-head>
            <md-table-head>作成日</md-table-head>
            <md-table-head>最終カード利用日</md-table-head>
            <md-table-head>編集</md-table-head>
            <md-table-head>削除</md-table-head>
          </md-table-row>

          <md-table-row v-for="(item, index) in items.monitor_user" :key="item.card_number">
            <md-table-cell>{{ item.monitor_user_name }}</md-table-cell>
            <md-table-cell>{{ item.monitor_email }}</md-table-cell>
            <md-table-cell>{{ item.created_at }}</md-table-cell>
            <md-table-cell>{{ item.last_used_date }}</md-table-cell>
            <md-table-cell>
              <md-button class="md-info" @click="editDataSwitch(index), editData(index)" :disabled="edit != null">編集</md-button>
            </md-table-cell>
            <md-table-cell>
              <md-button class="md-danger" @click="onAlert(index)" :disabled="edit != null">削除</md-button>
            </md-table-cell>
          </md-table-row>
        </md-table>
      </div>
    </md-card-content>
  </md-card>
  <div v-if="edit != null">
    <md-card id="edit">
      <md-card-header data-background-color="blue">
        <h4 class="title">ユーザー編集</h4>
      </md-card-header>
      <md-card-content>
        <span class="error" v-if="
              $v.editMonitorUserName.$invalid && $v.editMonitorUserName.$dirty
            ">必須項目です</span>
        <md-field>
          <label>保護者名</label>
          <md-input v-model="editMonitorUserName" @blur="$v.editMonitorUserName.$touch()"></md-input>
        </md-field>

        <span class="error" v-if="!$v.editEmail.email && $v.editEmail.$dirty">正しいメールアドレスを入力してください</span>
        <md-field>
          <label>メールアドレス</label>
          <md-input v-model="editEmail" @blur="$v.editEmail.$touch()"></md-input>
        </md-field>

        <span class="error" v-if="
              $v.editMonitorTargetUserName.$invalid &&
              $v.editMonitorTargetUserName.$dirty
            ">必須項目です</span>
        <md-field>
          <label>見守り対象名</label>
          <md-input v-model="editMonitorTargetUserName" @blur="$v.editMonitorTargetUserName.$touch()"></md-input>
        </md-field>

        <span class="error" v-if="!$v.editCardNumber.required && $v.editCardNumber.$dirty">必須項目です</span>
        <span class="error" v-if="
              (!$v.editCardNumber.alphaNum ||
                !$v.editCardNumber.minLength ||
                !$v.editCardNumber.maxLength) &&
              $v.editCardNumber.$dirty
            ">英数字16桁で入力してください</span>
        <md-field>
          <label>カード番号</label>
          <md-input v-model="editCardNumber" @blur="$v.editCardNumber.$touch()"></md-input>
        </md-field>
        <Right>
          <md-button class="md-size-20" @click="editDataSwitch(-1), reset()">編集取り消し</md-button>
          <md-button class="md-warning md-size-20" @click="editAdd(), editDataSwitch(-1), reset()" :disabled="
                $v.editMonitorUserName.$invalid ||
                $v.editEmail.$invalid ||
                $v.editMonitorTargetUserName.$invalid ||
                $v.editCardNumber.$invalid
              ">変更を保存</md-button>
        </Right>
      </md-card-content>
    </md-card>
  </div>
</div>
</template>
<script>
import {
  required,
  email,
  minLength,
  maxLength,
  alphaNum,
} from "vuelidate/lib/validators";
export default {
  data() {
    return {
      show: false,
      edit: null,
      items: [],
      monitorUserName: null,
      monitorTargetUserName: null,
      email: null,
      cardNumber: null,
      editMonitorUserName: null,
      editMonitorTargetUserName: null,
      editEmail: null,
      editCardNumber: null,
    };
  },
  methods: {
    /**
     * 新規ユーザーの登録画面の出力
     * @return {[type]} [description]
     */
    newUserSwitch() {
      if (this.show == false) {
        this.show = true;
      } else {
        this.show = false;
      }
    },

    /**
     * 編集画面の出力スイッチ
     * @param  {num} index
     */
    editDataSwitch(index) {
      if (this.edit == null) {
        this.edit = index;
        setTimeout(this.goToEdit, 100);
      } else {
        this.edit = null;
      }
    },

    /**
     * 登録，更新時にtextboxの値をクリアする
     */
    reset() {
      this.monitorUserName = null;
      this.monitorTargetUserName = null;
      this.cardNumber = null;
      this.email = null;
      this.editMonitorUserName = null;
      this.editMonitorTargetUserName = null;
      this.editEmail = null;
      this.editCardNumber = null;
    },

    /**
     * ユーザー登録時にAPIに値を送信
     */
    async add() {
      let url = "/web/monitor/management/register/";

      const data = {
        monitor_user_name: this.monitorUserName,
        monitor_email: this.email,
        monitor_target_user_name: this.monitorTargetUserName,
        card_number: this.cardNumber,
      };
      console.log(data);

      let result = await this.callPostAPI(url, data);

      url = "/web/monitor/management/";

      this.items = await this.callGetAPI(url, "");

      if ("message" in result) {
        this.notifyRegister(result.success, result.message);
      } else {
        this.notifyRegister(result.success);
      }
    },

    /**
     * 編集ボタンを押した際に，textboxに値を格納
     */
    editData(index) {
      this.editMonitorUserName = this.items.monitor_user[
        index
      ].monitor_user_name;
      this.editEmail = this.items.monitor_user[index].monitor_email;
      this.editMonitorTargetUserName = this.items.monitor_user[
        index
      ].monitor_target_user_name;
      this.editCardNumber = this.items.monitor_user[index].card_number;
    },

    /**
     * ユーザー更新処理
     */
    async editAdd() {
      let url = "/web/monitor/management/update/";

      const data = {
        user_id: this.items.monitor_user[this.edit].user_id,
        monitor_user_name: this.editMonitorUserName,
        monitor_email: this.editEmail,
        card_number: this.editCardNumber,
        monitor_target_user_name: this.editMonitorTargetUserName,
      };

      let result = await this.callPostAPI(url, data);

      url = "/web/monitor/management/";

      this.items = await this.callGetAPI(url, "");

      if ("message" in result) {
        this.notifyUpdate(result.success, result.message);
      } else {
        this.notifyUpdate(result.success);
      }
    },

    /**
     * ユーザー削除用関数
     * @param  {string}  user_id
     */
    async deleteUser(user_id) {
      let url = "/web/monitor/management/delete/";

      let data = {
        user_id: user_id,
      };

      let result = await this.callPostAPI(url, data);

      url = "/web/monitor/management/";
      this.items = await this.callGetAPI(url, "");

      this.notifyDelete(result.success);
    },

    /**
     * ユーザー削除用のモーダル表示
     * @param  {[type]} index 削除ボタン位置を示すindex
     */
    onAlert(index) {
      let message = {
        title: "確認",
        body: "この利用者情報を削除してもよろしいですか",
      };

      let options = {
        okText: "削除",
        cancelText: "キャンセル",
        backdropClose: true,
      };

      this.$dialog
        .confirm(message, options)
        .then(() => {
          this.deleteUser(this.items.monitor_user[index].user_id);
        })
        .catch(function() {
          console.log("Cancel delete");
        });
    },
  },
  async mounted() {
    let url = "/web/monitor/management/";
    this.items = await this.callGetAPI(url, "");
  },
  validations: {
    // 登録
    monitorUserName: {
      required,
    },
    email: {
      required,
      email,
    },
    monitorTargetUserName: {
      required,
    },
    cardNumber: {
      required,
      alphaNum,
      minLength: minLength(16),
      maxLength: maxLength(16),
    },
    //編集
    editMonitorUserName: {
      required,
    },
    editEmail: {
      required,
      email,
    },
    editMonitorTargetUserName: {
      required,
    },
    editCardNumber: {
      required,
      alphaNum,
      minLength: minLength(16),
      maxLength: maxLength(16),
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
