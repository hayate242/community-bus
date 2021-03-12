<template>
<div>
  <Right v-if="show == false">
    <md-button class="md-info md-layout-item md-size-20" @click="newUserSwitch()">新規運転手登録</md-button>
  </Right>
  <div v-if="this.show == true">
    <md-card>
      <md-card-header data-background-color="blue">
        <h4 class="title">新規運転手登録</h4>
      </md-card-header>
      <md-card-content>
        <span class="error" v-if="$v.driverName.$invalid && $v.driverName.$dirty">必須項目です</span>
        <md-field>
          <label>運転手名</label>
          <md-input v-model="driverName" @blur="$v.driverName.$touch()"></md-input>
        </md-field>

        <span class="error" v-if="!$v.email.required && $v.email.$dirty">必須項目です</span>
        <span class="error" v-if="!$v.email.email && $v.email.$dirty">正しいメールアドレスを入力してください</span>
        <md-field>
          <label>メールアドレス</label>
          <md-input v-model="email" @blur="$v.email.$touch()"></md-input>
        </md-field>

        <md-field>
          <label>パスワード</label>
          <md-input type="password" v-model="password"></md-input>
        </md-field>
        <Right>
          <md-button class="md-size-20" @click="newUserSwitch(), reset()">登録取り消し</md-button>
          <md-button class="md-warning md-size-20" @click="newUserSwitch(), add(), reset()" :disabled="$v.driverName.$invalid || $v.email.$invalid">登録確定</md-button>
        </Right>
      </md-card-content>
    </md-card>
  </div>
  <md-card>
    <md-card-header data-background-color="green">
      <h4 class="title">運転手一覧</h4>
    </md-card-header>
    <md-card-content>
      <div class="md-layout-item md-size-100">
        <md-table v-model="items">
          <md-table-row>
            <md-table-head>運転手名</md-table-head>
            <md-table-head>メールアドレス</md-table-head>
            <md-table-head>編集</md-table-head>
            <md-table-head>削除</md-table-head>
          </md-table-row>

          <md-table-row v-for="(item, index) in items.drivers" :key="item.driver_id">
            <md-table-cell>{{ item.driver_name }}</md-table-cell>
            <md-table-cell>{{ item.email }}</md-table-cell>
            <md-table-cell>
              <div v-if="edit == null">
                <md-button class="md-info" @click="editDataSwitch(index), editData(index)">編集</md-button>
              </div>
              <div v-else>
                <md-button class="md-info" @click="editDataSwitch(index), editData(index)" disabled>編集</md-button>
              </div>
            </md-table-cell>
            <md-table-cell>
              <div v-if="edit == null">
                <md-button class="md-danger" @click="onAlert(index)">削除</md-button>
              </div>
              <div v-else>
                <md-button class="md-danger" @click="onAlert(index)" disabled>削除</md-button>
              </div>
            </md-table-cell>
          </md-table-row>
        </md-table>
      </div>
    </md-card-content>
  </md-card>

  <div v-if="edit != null">
    <md-card id="edit">
      <md-card-header data-background-color="blue">
        <h4 class="title">運転手編集</h4>
      </md-card-header>
      <md-card-content>
        <span class="error" v-if="$v.editDriverName.$invalid && $v.editDriverName.$dirty">必須項目です</span>
        <md-field>
          <label>運転手名</label>
          <md-input v-model="editDriverName" @blur="$v.editDriverName.$touch()"></md-input>
        </md-field>

        <span class="error" v-if="!$v.editEmail.required && $v.editEmail.$dirty">必須項目です</span>
        <span class="error" v-if="!$v.editEmail.email && $v.editEmail.$dirty">正しいメールアドレスを入力してください</span>
        <md-field>
          <label>メールアドレス</label>
          <md-input v-model="editEmail" @blur="$v.editEmail.$touch()"></md-input>
        </md-field>

        <md-field>
          <label>パスワード</label>
          <md-input type="password" v-model="editPassword"></md-input>
        </md-field>
        <Right>
          <md-button class="md-size-20" @click="editDataSwitch(-1), reset()">編集取り消し</md-button>
          <md-button class="md-warning md-size-20" @click="editAdd(), editDataSwitch(-1), reset()" :disabled="$v.editDriverName.$invalid || $v.editEmail.$invalid">変更を保存</md-button>
        </Right>
      </md-card-content>
    </md-card>
  </div>
</div>
</template>
<script>
import {
  required,
  email
} from "vuelidate/lib/validators";
import axios from "axios";
export default {
  data() {
    return {
      show: false,
      driverName: null,
      email: null,
      password: null,
      editDriverName: null,
      editEmail: null,
      editPassword: "",
      edit: null,
      items: [],
    };
  },
  methods: {
    newUserSwitch() {
      if (this.show == false) {
        this.show = true;
      } else {
        this.show = false;
      }
    },
    editDataSwitch(index) {
      if (this.edit == null) {
        this.edit = index;
        setTimeout(this.goToEdit, 100);
      } else {
        this.edit = null;
      }
    },
    reset() {
      this.driverName = null;
      this.email = null;
      this.password = null;
    },
    /**
     * 運転手の新規登録処理
     */
    async add() {
      const data = {
        driver_name: this.driverName,
        email: this.email,
        password: this.password,
      };

      let url = "/web/drivers/register/";
      let result = await this.callPostAPI(url, data);
      if ("message" in result) {
        this.notifyRegister(result.success, result.message);
      } else {
        this.notifyRegister(result.success);
      }

      // 更新処理
      if (result.success == true) {
        //一覧データの更新処理
        let url = "/web/drivers/";
        this.items = await this.callGetAPI(url, "");
      }
    },
    editData(index) {
      this.editDriverName = this.items.drivers[index].driver_name;
      this.editEmail = this.items.drivers[index].email;
    },
    async editAdd() {
      const data = {
        driver_id: this.items.drivers[this.edit].driver_id + "",
        driver_name: this.editDriverName,
        email: this.editEmail,
        password: this.editPassword,
      };

      //更新用APIを叩く
      let url = "/web/drivers/update/";
      let result = await this.callPostAPI(url, data);
      if ("message" in result) {
        this.notifyUpdate(result.success, result.message);
      } else {
        this.notifyUpdate(result.success);
      }
      if (result.success == true) {
        //更新に成功した際
        let url = "/web/drivers/";
        this.items = await this.callGetAPI(url, "");
      }
    },

    /**
     * 運転手の削除
     * @param  {[type]} index 運転手id
     */
    async deleteItem(index) {
      const data = {
        driver_id: index + "",
      };

      let url = "/web/drivers/delete/";
      let result = await this.callPostAPI(url, data);
      this.notifyDelete(result.success);
      if (result.success == true) {
        url = "/web/drivers/";
        this.items = await this.callGetAPI(url, "");
      }
    },
    onAlert(index) {
      let message = {
        title: "確認",
        body: "この運転手情報を削除してもよろしいですか",
      };

      let options = {
        okText: "削除",
        cancelText: "キャンセル",
        backdropClose: true,
      };

      this.$dialog
        .confirm(message, options)
        .then(() => {
          this.deleteItem(this.items.drivers[index].driver_id);
        })
        .catch(function() {
          console.log("Cancel delete");
        });
    },
  },
  async mounted() {
    let url = "/web/drivers/";
    this.items = await this.callGetAPI(url, "");
  },
  validations: {
    driverName: {
      required,
    },
    email: {
      required,
      email,
    },
    editDriverName: {
      required,
    },
    editEmail: {
      required,
      email,
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
