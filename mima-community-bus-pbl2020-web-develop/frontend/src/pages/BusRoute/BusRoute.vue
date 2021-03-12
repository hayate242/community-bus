<template>
  <div class="md-layout">
    <div class="md-layout-item md-size-100">
      <!-- 新規用モーダル -->
      <modal name="new" height="auto" scrollable>
        <div class="modal-body">
          <md-card>
            <md-card-header data-background-color="blue">
              <h2 class="title">時刻設定</h2>
            </md-card-header>
            <md-card-content>
              <span class="error" v-if="!$v.order.required && $v.order.$dirty"
                >必須項目です</span
              >
              <span class="error" v-if="!$v.order.numeric && $v.order.$dirty"
                >数値を入力してください</span
              >
              <md-field>
                <label>便数</label>
                <md-input v-model="order" @blur="$v.order.$touch()"></md-input>
              </md-field>
              <md-table v-model="routes">
                <div v-for="items in routes.routes" :key="items.id">
                  <div v-if="items.id == routeId">
                    <md-table-row
                      v-for="(item, index) in items.route"
                      :key="index"
                    >
                      <md-table-cell>{{ item.name }}</md-table-cell>
                      <md-table-cell class="custom-width">
                        <div v-if="routeDetail[index].is_used == true">
                          <VueCtkDateTimePicker
                            id="index"
                            v-model="routeDetail[index].time"
                            label="到着予定時刻"
                            format="HH:mm"
                            formatted="HH:mm"
                            only-time
                            overlay
                            inline
                          />
                        </div>
                        <div v-else>
                          <p>このバス停は利用しません.</p>
                        </div>
                      </md-table-cell>
                      <md-table-cell>
                        <div v-if="routeDetail[index].is_used == true">
                          <md-button class="md-denger" @click="switchUse(index)"
                            >このバス停を利用しない</md-button
                          >
                        </div>
                        <div v-else>
                          <md-button class="md-info" @click="switchUse(index)"
                            >このバス停を利用する</md-button
                          >
                        </div>
                      </md-table-cell>
                    </md-table-row>
                  </div>
                </div>
              </md-table>
              <Right>
                <md-button @click="hideModal">取り消し</md-button>
                <md-button
                  class="md-warning"
                  @click="addNewCourse(), hideModal()"
                  :disabled="$v.order.$invalid"
                  >登録</md-button
                >
              </Right>
            </md-card-content>
          </md-card>
        </div>
      </modal>

      <!-- 編集用モーダル -->
      <modal name="edit" height="auto" scrollable>
        <div class="modal-body">
          <md-card>
            <md-card-header data-background-color="blue">
              <h2 class="title">時刻設定編集</h2>
            </md-card-header>
            <md-card-content>
              <span class="error" v-if="$v.order.$invalid && $v.order.$dirty"
                >必須項目です</span
              >
              <span class="error" v-if="!$v.order.numeric && $v.order.$dirty"
                >数値を入力してください</span
              >
              <md-field>
                <label>便数</label>
                <md-input v-model="order" @blur="$v.order.$touch()"></md-input>
              </md-field>
              <md-table v-model="routes">
                <md-table-row v-for="(item, index) in routeDetail" :key="index">
                  <md-table-cell>{{ item.name }}</md-table-cell>
                  <md-table-cell class="custom-width">
                    <div v-if="item.is_used == true">
                      <VueCtkDateTimePicker
                        id="index"
                        v-model="routeDetail[index].time"
                        label="到着予定時刻"
                        format="HH:mm"
                        formatted="HH:mm"
                        only-time
                        overlay
                        inline
                      />
                    </div>
                    <div v-else>
                      <p>このバス停は利用しません.</p>
                    </div>
                  </md-table-cell>
                  <md-table-cell>
                    <div v-if="item.is_used == true">
                      <md-button class="md-denger" @click="switchUse(index)"
                        >このバス停を利用しない</md-button
                      >
                    </div>
                    <div v-else>
                      <md-button class="md-info" @click="switchUse(index)"
                        >このバス停を利用する</md-button
                      >
                    </div>
                  </md-table-cell>
                </md-table-row>
              </md-table>
              <Right>
                <md-button @click="hideModal">取り消し</md-button>
                <md-button
                  class="md-warning"
                  @click="addEditCourse(), hideModal()"
                  :disabled="$v.order.$invalid"
                  >登録</md-button
                >
              </Right>
            </md-card-content>
          </md-card>
        </div>
      </modal>
      <nav-tabs-card>
        <template slot="content">
          <md-tabs md-sync-route class="md-success" md-alignment="left">
            <md-tab id="busStop" md-label="バス停・通過ポイント" to="#busStop">
              <BusStop :busStop="busStop" @updateAPI="updateAPI" />
            </md-tab>

            <md-tab id="route" md-label="路線" to="#route">
              <Route
                :busStop="busStop"
                :routes="routes"
                @updateAPI="updateAPI"
              />
            </md-tab>

            <md-tab id="course" md-label="コース" to="#course">
              <Course
                :busStop="busStop"
                :routes="routes"
                :courses="courses"
                :newCourse="newCourse"
                @showModal="showModal"
                @showEditModal="showEditModal"
                @updateAPI="updateAPI"
                ref="addCourse"
              />
            </md-tab>
          </md-tabs>
        </template>
      </nav-tabs-card>
    </div>
  </div>
</template>

<script>
import BusStop from "./BusStop.vue";
import Route from "./Route.vue";
import Course from "./Course.vue";
import { required, numeric } from "vuelidate/lib/validators";

export default {
  data() {
    return {
      routeId: null,
      routeDetail: [],
      busStop: {},
      routes: {},
      courses: {},
      newCourse: [],
      button: null,
      route: null,
      index: null,
      order: null,
    };
  },
  components: {
    BusStop,
    Route,
    Course,
  },
  methods: {
    /**
     * コースタブの時刻入力時のモーダルを表示する関数
     * @param  {num} routeId 路線id
     * @param  {num} button 謳歌されたボタンの種類
     */
    showModal(routeId, button) {
      this.button = button;
      this.makeRouteDetail(routeId, 0);
      this.routeId = routeId;
      this.order = null;
      this.$modal.show("new");
    },

    /**
     * 編集用のモーダル表示
     * @param  {num} index  編集するコースのindex
     * @param  {Object} route  編集するコースの情報
     * @param  {num} button 新規作成(0)かコース編集(1)か
     */
    async showEditModal(index, route, button) {
      this.routeId = route.id;
      this.route = route;
      this.button = button;
      this.index = index;
      await this.makeRouteDetail(this.routeId, 1);
      this.order = route.order;
      try {
        this.$modal.show("edit");
      } catch (e) {
        console.log("modal error");
      }
    },

    /**
     * コースタブの時刻入力時のモーダルを消す関数
     */
    hideModal() {
      this.$modal.hide("new");
      this.$modal.hide("edit");
    },

    /**
     * モーダル上のこのバス停を利用するボタンとこのバス停を利用しないボタンを切り替える
     * @param  {num} index ボタンの位置のindex
     */
    switchUse(index) {
      if (this.routeDetail[index].is_used == false) {
        this.routeDetail[index].is_used = true;
      } else {
        this.routeDetail[index].is_used = false;
      }
    },
    /**
    * モーダルに表示するバス停の利用の有無と時刻設定をrouteDetailに格納
    @param {num} routeId 路線id
    */
    makeRouteDetail(routeId, flg) {
      this.routeDetail = [];
      var route = null;
      for (var i = 0; i < this.routes.routes.length; i++) {
        if (this.routes.routes[i].id == routeId) {
          console.log("1");
          route = this.routes.routes[i];
          break;
        }
      }
      if (flg == 0) {
        for (var i = 0; i < route.route.length; i++) {
          this.routeDetail.push({
            id: route.route[i].id,
            name: route.route[i].name,
            time: "00:00",
            is_used: true,
            order: String(i + 1),
          });
        }
      } else {
        console.log(this.route);
        for (var i = 0; i < this.route.route.length; i++) {
          this.routeDetail.push({
            id: this.route.route[i].id,
            name: this.route.route[i].name,
            time: this.route.route[i].time,
            is_used: this.route.route[i].is_used,
            order: String(i + 1),
          });
        }
      }
    },

    /**
     * コースの新規作成時，作成するコース欄に新たなルートを追加する関数
     */
    addNewCourse() {
      var route = null;
      for (var i = 0; this.routes.routes.length; i++) {
        if (this.routes.routes[i].id == this.routeId) {
          route = this.routes.routes[i];
          break;
        }
      }
      this.$refs.addCourse.addCourse(
        route,
        this.routeDetail,
        this.button,
        this.order
      ); //Course.vueコンポーネントのaddCourseコンポーネントを呼び出して，子のcourse変数に値を格納する
    },

    /**
     * コースの編集時，作成するコース欄の情報を変更
     */
    addEditCourse() {
      var route = null;
      for (var i = 0; this.routes.routes.length; i++) {
        if (this.routes.routes[i].id == this.routeId) {
          route = this.routes.routes[i];
          break;
        }
      }
      this.$refs.addCourse.addEditRoute(
        this.index,
        route,
        this.routeDetail,
        this.button,
        this.order
      );
    },

    /**
     * バス停，路線，コースのAPIを更新
     */
    async updateAPI() {
      var url = "";
      //バス停を更新
      url = "/web/busStop/";
      this.busStop = await this.callGetAPI(url, "");

      //路線を更新
      url = "/web/route/";
      this.routes = await this.callGetAPI(url, "");

      //コースを更新
      url = "/web/course/";
      this.courses = await this.callGetAPI(url, "");
    },
  },
  /**
   * 画面生成時にAPIを叩いてバス停，路線，コースを取得する
   */
  async mounted() {
    //バス停のAPIを叩く
    let url = "/web/busStop/";
    this.busStop = await this.callGetAPI(url, "");

    //路線のAPI叩く
    url = "/web/route/";
    this.routes = await this.callGetAPI(url, "");

    //コースのAPIを叩く
    url = "/web/course/";
    this.courses = await this.callGetAPI(url, "");
  },
  validations: {
    order: {
      required,
      numeric,
    },
  },
};
</script>

<style>
.custom-width {
  width: 200px;
}

.error {
  color: #8a0421;
  border-color: #dd0f3b;
  background-color: #ffd9d9;
}
</style>
