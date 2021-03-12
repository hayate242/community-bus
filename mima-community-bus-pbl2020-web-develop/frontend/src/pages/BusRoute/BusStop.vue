<template>
  <div>
    <!-- 新規バス停ボタン -->
    <Right v-if="show == false">
      <md-button
        class="md-info md-layout-item md-size-20"
        @click="newerSwitch()"
        >新規バス停・通過ポイント登録</md-button
      >
    </Right>

    <!-- 新規バス停情報入力欄 -->
    <!-- TODO: mapから緯度経度を入力できるようにする -->
    <div v-if="this.show == true">
      <md-card>
        <md-card-header data-background-color="blue">
          <h4 class="title">新規バス停・通過ポイント登録</h4>
        </md-card-header>
        <md-card-content>
          <span class="error" v-if="$v.name.$invalid && $v.name.$dirty"
            >必須項目です</span
          >
          <md-field>
            <label>バス停・通過ポイント名</label>
            <md-input v-model="name" @blur="$v.name.$touch()"></md-input>
          </md-field>

          <span class="error" v-if="!$v.latitude.required && $v.latitude.$dirty"
            >必須項目です</span
          >
          <span class="error" v-if="!$v.latitude.between && $v.latitude.$dirty"
            >正しい数値を入力してください</span
          >
          <md-field>
            <label>緯度</label>
            <md-input
              v-model="latitude"
              @blur="$v.latitude.$touch()"
            ></md-input>
          </md-field>

          <span
            class="error"
            v-if="!$v.longitude.required && $v.longitude.$dirty"
            >必須項目です</span
          >
          <span
            class="error"
            v-if="!$v.longitude.between && $v.longitude.$dirty"
            >正しい数値を入力してください</span
          >
          <md-field>
            <label>経度</label>
            <md-input
              v-model="longitude"
              @blur="$v.longitude.$touch()"
            ></md-input>
          </md-field>
          <md-checkbox v-model="isPassingPoint"
            >通過ポイントとして登録する</md-checkbox
          >
          <Right>
            <md-button class="md-size-20" @click="newerSwitch(), reset()"
              >登録取り消し</md-button
            >
            <md-button
              class="md-warning md-size-20"
              @click="newerSwitch(), add(), reset()"
              :disabled="
                $v.name.$invalid ||
                $v.latitude.$invalid ||
                $v.longitude.$invalid
              "
              >登録確定</md-button
            >
          </Right>
        </md-card-content>
      </md-card>
    </div>

    <!-- バス停一覧 -->
    <md-card>
      <md-card-header data-background-color="green">
        <h4 class="title">バス停・通過ポイント一覧</h4>
      </md-card-header>
      <md-card-content>
        <div class="md-layout-item md-size-100">
          <md-table v-model="busStop">
            <md-table-row>
              <md-table-head>バス停・通過ポイント名</md-table-head>
              <md-table-head>種別</md-table-head>
              <md-table-head>利用路線</md-table-head>
              <md-table-head>緯度</md-table-head>
              <md-table-head>経度</md-table-head>
              <md-table-head>編集</md-table-head>
              <md-table-head>削除</md-table-head>
            </md-table-row>

            <md-table-row
              v-for="(item, index) in busStop.bus_stop"
              :key="item.id"
            >
              <md-table-cell
                ><a
                  :href="getGoogleMarkerLink(item.latitude, item.longitude)"
                  target="_blank"
                  rel="noopener noreferrer"
                  >{{ item.name }}</a
                ></md-table-cell
              >
              <md-table-cell>
                <div v-if="item.is_passing_point == false">バス停</div>
                <div v-else>通過ポイント</div>
              </md-table-cell>
              <md-table-cell>
                <div
                  v-for="(used_item, used_item_index) in item.used_by"
                  :key="used_item_index"
                >
                  {{ used_item }}
                </div>
              </md-table-cell>
              <md-table-cell>{{ item.latitude }}</md-table-cell>
              <md-table-cell>{{ item.longitude }}</md-table-cell>
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
                <div v-if="edit == null && item.used_by.length == 0">
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

    <!-- バス停編集 -->
    <div v-if="edit != null">
      <md-card id="edit">
        <md-card-header data-background-color="blue">
          <h4 class="title">バス停・通過ポイント編集</h4>
        </md-card-header>
        <md-card-content>
          <span class="error" v-if="$v.editName.$invalid && $v.editName.$dirty"
            >必須項目です</span
          >
          <md-field>
            <label>バス停・通過ポイント名</label>
            <md-input
              v-model="editName"
              @blur="$v.editName.$touch()"
            ></md-input>
          </md-field>

          <span
            class="error"
            v-if="!$v.editLatitude.required && $v.editLatitude.$dirty"
            >必須項目です</span
          >
          <span
            class="error"
            v-if="!$v.editLatitude.between && $v.editLatitude.$dirty"
            >正しい数値を入力してください</span
          >
          <md-field>
            <label>緯度</label>
            <md-input
              v-model="editLatitude"
              @blur="$v.editLatitude.$touch()"
            ></md-input>
          </md-field>

          <span
            class="error"
            v-if="!$v.editLongitude.required && $v.editLongitude.$dirty"
            >必須項目です</span
          >
          <span
            class="error"
            v-if="!$v.editLongitude.between && $v.editLongitude.$dirty"
            >正しい数値を入力してください</span
          >
          <md-field>
            <label>経度</label>
            <md-input
              v-model="editLongitude"
              @blur="$v.editLongitude.$touch()"
            ></md-input>
          </md-field>
          <md-checkbox v-model="editIsPassingPoint"
            >通過ポイントとして登録する</md-checkbox
          >
          <Right>
            <md-button class="md-size-20" @click="editDataSwitch(-1), reset()"
              >編集取り消し</md-button
            >
            <md-button
              class="md-warning md-size-20"
              @click="editAdd(), editDataSwitch(-1), reset()"
              :disabled="
                $v.editName.$invalid ||
                $v.editLatitude.$invalid ||
                $v.editLongitude.$invalid
              "
              >変更を保存</md-button
            >
          </Right>
        </md-card-content>
      </md-card>
    </div>
  </div>
</template>
<script>
import { required, between } from "vuelidate/lib/validators";
export default {
  props: {
    busStop: {
      type: Object,
    },
  },
  data() {
    return {
      show: false,
      name: null,
      longitude: null,
      latitude: null,
      editName: null,
      editLongitude: null,
      editLatitude: null,
      edit: null,
      isPassingPoint: false,
      editIsPassingPoint: false,
    };
  },
  methods: {
    newerSwitch() {
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

    editData(index) {
      this.editName = this.busStop.bus_stop[index].name;
      this.editLongitude = this.busStop.bus_stop[index].longitude;
      this.editLatitude = this.busStop.bus_stop[index].latitude;
      this.editIsPassingPoint = this.busStop.bus_stop[index].is_passing_point;
    },
    reset() {
      this.name = null;
      this.longitude = null;
      this.latitude = null;
      this.isPassingPoint = false;
    },
    getGoogleMarkerLink(lat, lng) {
      return "https://maps.google.com/maps?q=" + lat + "," + lng;
    },
    async add() {
      //APIを叩く処理
      const data = {
        bus_stop_name: this.name,
        longitude: this.longitude,
        latitude: this.latitude,
        is_passing_point: this.isPassingPoint,
      };

      let url = "/web/busStop/register/";
      let result = await this.callPostAPI(url, data);
      this.notifyRegister(result.success);
      //更新処理
      this.updateAPI();
    },
    async editAdd() {
      const data = {
        id: this.busStop.bus_stop[this.edit].id,
        bus_stop_name: this.editName,
        latitude: this.editLatitude,
        longitude: this.editLongitude,
        is_passing_point: this.editIsPassingPoint,
      };

      let url = "/web/busStop/update/";
      let result = await this.callPostAPI(url, data);
      this.notifyUpdate(result.success);
      this.updateAPI();
    },
    /**
     * バス停を削除し，バス停一覧データを更新する関数
     * @param  {num}  index 削除するバス停id
     */
    async deleteItem(index) {
      const data = {
        bus_stop_id: index,
      };

      let url = "/web/busStop/delete/";
      let result = await this.callPostAPI(url, data);
      console.log("success=" + result.success);
      this.notifyDelete(result.success);
      this.updateAPI();
    },
    onAlert(index) {
      let message = {
        title: "確認",
        body: "このバス停情報を削除してもよろしいですか",
      };

      let options = {
        okText: "削除",
        cancelText: "キャンセル",
        backdropClose: true,
      };

      this.$dialog
        .confirm(message, options)
        .then(() => {
          this.deleteItem(this.busStop.bus_stop[index].id);
        })
        .catch(function () {
          console.log("Cancel delete");
        });
    },

    /**
     * バス停，路線，コースのAPIを更新
     * @param  {num} flg 0:バス停，1:路線，2:コースを更新
     */
    updateAPI() {
      this.$emit("updateAPI");
      this.$router.go({
        path: this.$router.currentRoute.path,
        force: true,
      });
    },
  },
  validations: {
    name: {
      required,
    },
    longitude: {
      required,
      between: between(-180, 180),
    },
    latitude: {
      required,
      between: between(-90, 90),
    },
    editName: {
      required,
    },
    editLongitude: {
      required,
      between: between(-180, 180),
    },
    editLatitude: {
      required,
      between: between(-90, 90),
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
