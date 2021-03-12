<template>
<div>
  <!-- 新規路線ボタン -->
  <Right v-if="show == false">
    <md-button class="md-info md-layout-item md-size-20" @click="newerSwitch()">新規路線登録</md-button>
  </Right>

  <!-- 新規路線入力欄 -->
  <div v-if="this.show == true">
    <md-card>
      <md-card-header data-background-color="blue">
        <h4 class="title">新規路線登録</h4>
      </md-card-header>
      <md-card-content>
        <span class="error" v-if="$v.routeName.$invalid && $v.routeName.$dirty">必須項目です</span>
        <md-field>
          <label>路線名</label>
          <md-input v-model="routeName" @blur="$v.routeName.$touch()"></md-input>
        </md-field>

        <!-- 登録可能バス停一覧 -->
        <div class="md-layout">
          <md-card class="md-layout-item">
            <md-card-header data-background-color="blue">
              <h4 class="titel">バス停リスト</h4>
            </md-card-header>
            <md-card-content>
              <md-table v-model="busStop">
                <md-table-row>
                  <md-table-head>バス停名</md-table-head>
                  <md-table-head>追加ボタン</md-table-head>
                </md-table-row>
                <md-table-row v-for="(item, index) in busStop.bus_stop" :key="item.id">
                  <md-table-cell>{{ item.name }}</md-table-cell>
                  <md-table-cell>
                    <md-button class="md-info" @click="addRoute(index)">追加</md-button>
                  </md-table-cell>
                </md-table-row>
              </md-table>
            </md-card-content>
          </md-card>

          <!-- 作成している路線 -->
          <md-card class="md-layout-item">
            <md-card-header data-background-color="blue">
              <h4 class="titel">作成する路線</h4>
            </md-card-header>
            <md-card-content>
              <md-table v-model="route">
                <draggable v-model="route">
                  <md-table-row v-for="(item, index) in route" :key="index">
                    <md-table-cell>{{ index + 1 }}.</md-table-cell>
                    <md-table-cell>{{ item.name }}</md-table-cell>
                    <md-table-cell>
                      <md-button class="md-danger" @click="deleteBusStop(index)">削除</md-button>
                    </md-table-cell>
                  </md-table-row>
                </draggable>
              </md-table>
            </md-card-content>
          </md-card>
        </div>

        <!-- 登録ボタン -->
        <Right>
          <md-button class="md-size-20" @click="newerSwitch(), reset()">登録取り消し</md-button>
          <md-button class="md-warning md-size-20" @click="newerSwitch(), add(), reset()" :disabled="$v.routeName.$invalid">登録確定</md-button>
        </Right>
      </md-card-content>
    </md-card>
  </div>

  <!-- 路線一覧 -->
  <md-card>
    <md-card-header data-background-color="green">
      <h4 class="title">路線一覧</h4>
    </md-card-header>
    <md-card-content>
      <div class="md-layout-item md-size-100">
        <md-table v-model="routes">
          <md-table-row>
            <md-table-head>路線名</md-table-head>
            <md-table-head>利用コース</md-table-head>
            <md-table-head>編集</md-table-head>
            <md-table-head>削除</md-table-head>
          </md-table-row>

          <md-table-row v-for="(item, index) in routes.routes" :key="item.id">
            <md-table-cell>{{ item.name }}</md-table-cell>
            <md-table-cell>
              <div v-for="(used_item, used_item_index) in item.used_by" :key="used_item_index">
                {{used_item}}
              </div>
            </md-table-cell>
            <md-table-cell>
              <div v-if="edit == null && item.used_by.length == 0">
                <md-button class="md-info" @click="editDataSwitch(index), editData(index)">編集</md-button>
              </div>
              <div v-else>
                <md-button class="md-info" @click="editDataSwitch(index), editData(index)" disabled>編集</md-button>
              </div>
            </md-table-cell>
            <md-table-cell>
              <div v-if="edit == null && item.used_by.length == 0">
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

  <!-- 路線編集 -->
  <div v-if="edit != null">
    <md-card id="edit">
      <md-card-header data-background-color="blue">
        <h4 class="title">路線編集</h4>
      </md-card-header>
      <md-card-content>
        <span class="error" v-if="$v.editRouteName.$invalid && $v.editRouteName.$dirty">必須項目です</span>
        <md-field>
          <label>路線名</label>
          <md-input v-model="editRouteName" @blur="$v.editRouteName.$touch()"></md-input>
        </md-field>
        <!-- 登録可能バス停一覧 -->
        <div class="md-layout">
          <md-card class="md-layout-item">
            <md-card-header data-background-color="blue">
              <h4 class="titel">バス停リスト</h4>
            </md-card-header>
            <md-card-content>
              <md-table v-model="busStop">
                <md-table-row>
                  <md-table-head>バス停名</md-table-head>
                  <md-table-head>追加ボタン</md-table-head>
                </md-table-row>
                <md-table-row v-for="(item, index) in busStop.bus_stop" :key="item.id">
                  <md-table-cell>{{ item.name }}</md-table-cell>
                  <md-table-cell>
                    <md-button class="md-info" @click="addEditRoute(index)">追加</md-button>
                  </md-table-cell>
                </md-table-row>
              </md-table>
            </md-card-content>
          </md-card>

          <!-- 作成している路線 -->
          <md-card class="md-layout-item">
            <md-card-header data-background-color="blue">
              <h4 class="titel">作成する路線</h4>
            </md-card-header>
            <md-card-content>
              <md-table v-model="editRoute">
                <draggable v-model="editRoute">
                  <md-table-row v-for="(item, index) in editRoute" :key="index">
                    <md-table-cell>{{ index + 1 }}.</md-table-cell>
                    <md-table-cell>{{ item.name }}</md-table-cell>
                    <md-table-cell>
                      <md-button class="md-danger" @click="deleteEditBusStop(index)">削除</md-button>
                    </md-table-cell>
                  </md-table-row>
                </draggable>
              </md-table>
            </md-card-content>
          </md-card>
        </div>

        <Right>
          <md-button class="md-size-20" @click="editDataSwitch(-1), editReset()">編集取り消し</md-button>
          <md-button class="md-warning md-size-20" @click="editAdd(), editDataSwitch(-1), editReset()" :disabled="$v.editRouteName.$invalid">変更を保存</md-button>
        </Right>
      </md-card-content>
    </md-card>
  </div>
</div>
</template>
<script>
import {
  required
} from "vuelidate/lib/validators";
export default {
  props: {
    busStop: {
      type: Object,
    },
    routes: {
      type: Object,
    },
  },
  data() {
    return {
      show: false,
      routeName: null,
      route: [],
      editRouteName: null,
      editRoute: [],
      edit: null,
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
      this.editRouteName = this.routes.routes[index].name;
      for (var i = 0; i < this.routes.routes[index].route.length; i++) {
        this.editRoute.push(this.routes.routes[index].route[i]);
      }
    },
    addEditRoute(index) {
      this.editRoute.push({
        id: this.busStop.bus_stop[index].id,
        name: this.busStop.bus_stop[index].name,
      });
    },
    reset() {
      this.route = [];
    },
    editReset() {
      this.editRoute = [];
    },
    addRoute(index) {
      this.route.push({
        id: this.busStop.bus_stop[index].id,
        name: this.busStop.bus_stop[index].name,
      });
    },
    async add() {
      const data = {
        name: this.routeName,
        route: this.route,
      };
      // orderを追加
      data.route = data.route.map(function(busStop, index) {
        return {
          id: busStop.id,
          name: busStop.name,
          order: String(index + 1),
        };
      });
      let url = "/web/route/register/";
      let result = await this.callPostAPI(url, data);
      this.notifyRegister(result.success);
      this.updateAPI();
    },
    async editAdd() {
      const data = {
        id: this.routes.routes[this.edit].id + "",
        name: this.editRouteName,
        route: this.editRoute,
      };
      // orderを追加
      data.route = data.route.map(function(busStop, index) {
        return {
          id: busStop.id,
          name: busStop.name,
          order: String(index + 1),
        };
      });
      let url = "/web/route/update/";
      let result = await this.callPostAPI(url, data);
      this.notifyUpdate(result.success);
      this.updateAPI();
    },
    deleteBusStop(index) {
      this.route.splice(index, 1);
    },
    deleteEditBusStop(index) {
      this.editRoute.splice(index, 1);
    },

    /**
     * 路線を削除し，路線データをAPIから受け取って更新する
     * @param  {num} index 路線のid
     */
    async deleteCourse(index) {
      const data = {
        route_id: index,
      };

      let url = "/web/route/delete/";
      let result = await this.callPostAPI(url, data);
      this.notifyDelete(result.success);
      this.updateAPI();
    },

    onAlert(index) {
      let message = {
        title: "確認",
        body: "この路線情報を削除してもよろしいですか",
      };

      let options = {
        okText: "削除",
        cancelText: "キャンセル",
        backdropClose: true,
      };

      this.$dialog
        .confirm(message, options)
        .then(() => {
          this.deleteCourse(this.routes.routes[index].id);
        })
        .catch(function() {
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
        force: true
      })
    },
  },
  validations: {
    routeName: {
      required,
    },
    editRouteName: {
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
