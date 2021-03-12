<template>
  <div>
    <Right v-if="show == false">
      <md-button
        class="md-info md-layout-item md-size-20"
        @click="newBusSwitch()"
        >新規車両登録</md-button
      >
    </Right>
    <div v-if="this.show == true">
      <md-card>
        <md-card-header data-background-color="blue">
          <h4 class="title">新規車両登録</h4>
        </md-card-header>
        <md-card-content>
          <span
            class="error"
            v-if="$v.busNumber.$invalid && $v.busNumber.$dirty"
            >必須項目です</span
          >
          <md-field>
            <label>車両ナンバー</label>
            <md-input
              v-model="busNumber"
              @blur="$v.busNumber.$touch()"
            ></md-input>
          </md-field>

          <span class="error" v-if="$v.busName.$invalid && $v.busName.$dirty"
            >必須項目です</span
          >
          <md-field>
            <label>車両名</label>
            <md-input v-model="busName" @blur="$v.busName.$touch()"></md-input>
          </md-field>
          <Right>
            <md-button class="md-size-20" @click="newBusSwitch(), reset()"
              >登録取り消し</md-button
            >
            <md-button
              class="md-warning md-size-20"
              @click="newBusSwitch(), add(), reset()"
              :disabled="$v.busNumber.$invalid || $v.busName.$invalid"
              >登録確定</md-button
            >
          </Right>
        </md-card-content>
      </md-card>
    </div>
    <md-card>
      <md-card-header data-background-color="green">
        <h4 class="title">車両一覧</h4>
      </md-card-header>
      <md-card-content>
        <div class="md-layout-item md-size-100">
          <md-table v-model="items">
            <md-table-row>
              <md-table-head>車両ナンバー</md-table-head>
              <md-table-head>車両名</md-table-head>
              <md-table-head>編集</md-table-head>
              <md-table-head>削除</md-table-head>
            </md-table-row>

            <md-table-row
              v-for="(item, index) in items.buses"
              :key="item.bus_number"
            >
              <md-table-cell>{{ item.bus_number }}</md-table-cell>
              <md-table-cell>{{ item.bus_name }}</md-table-cell>
              <md-table-cell>
                <div v-if="edit == null">
                  <md-button
                    class="md-info"
                    @click="editDataSwitch(index), editData(index)"
                    >編集</md-button
                  >
                </div>
                <div v-else>
                  <md-button
                    class="md-info"
                    @click="editDataSwitch(index), editData(index)"
                    disabled
                    >編集</md-button
                  >
                </div>
              </md-table-cell>
              <md-table-cell>
                <div v-if="edit == null">
                  <md-button class="md-danger" @click="onAlert(index)"
                    >削除</md-button
                  >
                </div>
                <div v-else>
                  <md-button class="md-danger" @click="onAlert(index)" disabled
                    >削除</md-button
                  >
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
          <h4 class="title">車両情報報編集</h4>
        </md-card-header>
        <md-card-content>
          <span
            class="error"
            v-if="$v.editBusNumber.$invalid && $v.editBusNumber.$dirty"
            >必須項目です</span
          >
          <md-field>
            <label>車両ナンバー</label>
            <md-input
              v-model="editBusNumber"
              @blur="$v.editBusNumber.$touch()"
            ></md-input>
          </md-field>

          <span
            class="error"
            v-if="$v.editBusName.$invalid && $v.editBusName.$dirty"
            >必須項目です</span
          >
          <md-field>
            <label>車両名</label>
            <md-input
              v-model="editBusName"
              @blur="$v.editBusName.$touch()"
            ></md-input>
          </md-field>
          <Right>
            <md-button class="md-size-20" @click="editDataSwitch(-1), reset()"
              >編集取り消し</md-button
            >
            <md-button
              class="md-warning md-size-20"
              @click="editAdd(), editDataSwitch(-1), reset()"
              :disabled="$v.editBusNumber.$invalid || $v.editBusName.$invalid"
              >変更を保存</md-button
            >
          </Right>
        </md-card-content>
      </md-card>
    </div>
  </div>
</template>
<script>
import { required } from "vuelidate/lib/validators";
export default {
  data() {
    return {
      show: false,
      busNumber: null,
      busName: null,
      editBusNumber: null,
      editBusName: null,
      edit: null,
      items: [],
    };
  },
  methods: {
    newBusSwitch() {
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
      this.busNumber = null;
      this.busName = null;
    },
    /**
     * バスの新規登録用関数
     */
    async add() {
      const data = {
        bus_number: this.busNumber,
        bus_name: this.busName,
      };

      let url = "/web/buses/register/";
      let result = await this.callPostAPI(url, data);
      this.notifyRegister(result.success);
      // 更新処理
      if (result.success == true) {
        //一覧データの更新処理
        let url = "/web/buses/";
        this.items = await this.callGetAPI(url, "");
      }
    },
    editData(index) {
      this.editBusNumber = this.items.buses[index].bus_number;
      this.editBusName = this.items.buses[index].bus_name;
    },
    /**
     * 変更を保存ボタンを押した際のupdate処理
     */
    async editAdd() {
      const data = {
        id: this.items.buses[this.edit].bus_id + "",
        bus_number: this.editBusNumber + "",
        bus_name: this.editBusName,
      };

      //更新用APIを叩く
      let url = "/web/buses/update/";
      let result = await this.callPostAPI(url, data);
      this.notifyUpdate(result.success);
      if (result.success == true) {
        //更新に成功した際
        let url = "/web/buses/";
        this.items = await this.callGetAPI(url, "");
      }
    },
    /**
     * 車両削除時の処理
     * @param  {string} index 車両ナンバー
     */
    async deleteItem(index) {
      const data = {
        id: index + "",
      };

      let url = "/web/buses/delete/";
      let result = await this.callPostAPI(url, data);
      this.notifyDelete(result.success);
      if (result.success == true) {
        url = "/web/buses/";
        this.items = await this.callGetAPI(url, "");
      }
    },
    onAlert(index) {
      let self = this;

      let message = {
        title: "確認",
        body: "この車両情報を削除してもよろしいですか",
      };

      let options = {
        okText: "削除",
        cancelText: "キャンセル",
        backdropClose: true,
      };

      this.$dialog
        .confirm(message, options)
        .then(function () {
          self.deleteItem(self.items.buses[index].bus_id);
        })
        .catch(function () {
          console.log("Cancel delete");
        });
    },
  },
  async mounted() {
    let url = "/web/buses/";
    this.items = await this.callGetAPI(url, "");
  },
  validations: {
    busNumber: {
      required,
    },
    busName: {
      required,
    },
    editBusNumber: {
      required,
    },
    editBusName: {
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
