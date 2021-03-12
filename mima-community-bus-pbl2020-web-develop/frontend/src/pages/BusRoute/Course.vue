<template>
<div>
  <!-- 新規路線ボタン -->
  <Right v-if="show == false">
    <md-button class="md-info md-layout-item md-size-20" @click="newerSwitch()">新規コース登録</md-button>
  </Right>

  <!-- 新規コース入力欄 -->
  <div v-if="this.show == true">
    <md-card>
      <md-card-header data-background-color="blue">
        <h4 class="title">新規コース登録</h4>
      </md-card-header>
      <md-card-content>
        <span class="error" v-if="$v.courseName.$invalid && $v.courseName.$dirty">必須項目です</span>
        <md-field>
          <label>コース名</label>
          <md-input v-model="courseName" @blur="$v.courseName.$touch()"></md-input>
        </md-field>

        <!-- 登録可能バス停一覧 -->
        <div class="md-layout">
          <md-card class="md-layout-item">
            <md-card-header data-background-color="blue">
              <h4 class="titel">路線リスト</h4>
            </md-card-header>
            <md-card-content>
              <md-table v-model="routes">
                <md-table-row>
                  <md-table-head>路線名</md-table-head>
                  <md-table-head>追加ボタン</md-table-head>
                </md-table-row>
                <md-table-row v-for="(item, index) in routes.routes" :key="item.id">
                  <md-table-cell>{{ item.name }}</md-table-cell>
                  <md-table-cell>
                    <md-button class="md-info" @click="showModal(index, 0)">追加</md-button>
                  </md-table-cell>
                </md-table-row>
              </md-table>
            </md-card-content>
          </md-card>

          <!-- 作成しているコース -->
          <md-card class="md-layout-item">
            <md-card-header data-background-color="blue">
              <h4 class="titel">作成するコース</h4>
            </md-card-header>
            <md-card-content>
              <md-table v-model="course">
                <draggable v-model="course">
                  <md-table-row v-for="(item, index) in course" :key="index">
                    <md-table-cell>{{ index + 1 }}.</md-table-cell>
                    <md-table-cell>{{
                        item.name + "  第" + item.order + "便"
                      }}</md-table-cell>
                    <md-table-cell>
                      <md-button class="md-info" @click="editRouteData(index, 0)">編集</md-button>
                      <md-button class="md-danger" @click="deleteRoute(index)">削除</md-button>
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
          <md-button class="md-warning md-size-20" @click="newerSwitch(), add(), reset()" :disabled="$v.courseName.$invalid">登録確定</md-button>
        </Right>
      </md-card-content>
    </md-card>
  </div>

  <!-- 路線一覧 -->
  <md-card>
    <md-card-header data-background-color="green">
      <h4 class="title">コース一覧</h4>
    </md-card-header>
    <md-card-content>
      <div class="md-layout-item md-size-100">
        <md-table v-model="courses">
          <md-table-row>
            <md-table-head>コース名</md-table-head>
            <md-table-head>編集</md-table-head>
            <md-table-head>削除</md-table-head>
          </md-table-row>

          <md-table-row v-for="(item, index) in courses.courses" :key="item.id">
            <md-table-cell>{{ item.name }}</md-table-cell>
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

  <!-- 路線編集 -->
  <div v-if="edit != null">
    <md-card id="edit">
      <md-card-header data-background-color="blue">
        <h4 class="title">コース編集</h4>
      </md-card-header>
      <md-card-content>
        <span class="error" v-if="$v.editCourseName.$invalid && $v.editCourseName.$dirty">必須項目です</span>
        <md-field>
          <label>コース名</label>
          <md-input v-model="editCourseName" @blur="$v.editCourseName.$touch()"></md-input>
        </md-field>
        <!-- 登録可能バス停一覧 -->
        <div class="md-layout">
          <md-card class="md-layout-item">
            <md-card-header data-background-color="blue">
              <h4 class="titel">路線リスト</h4>
            </md-card-header>
            <md-card-content>
              <md-table v-model="routes">
                <md-table-row>
                  <md-table-head>路線名</md-table-head>
                  <md-table-head>追加ボタン</md-table-head>
                </md-table-row>
                <md-table-row v-for="(item, index) in routes.routes" :key="item.id">
                  <md-table-cell>{{ item.name }}</md-table-cell>
                  <md-table-cell>
                    <md-button class="md-info" @click="showModal(index, 1)">追加</md-button>
                  </md-table-cell>
                </md-table-row>
              </md-table>
            </md-card-content>
          </md-card>

          <!-- 作成している路線 -->
          <md-card class="md-layout-item">
            <md-card-header data-background-color="blue">
              <h4 class="titel">編集するコース</h4>
            </md-card-header>
            <md-card-content>
              <md-table v-model="editCourse">
                <draggable v-model="editCourse">
                  <md-table-row v-for="(item, index) in editCourse" :key="index">
                    <md-table-cell>{{ index + 1 }}.</md-table-cell>
                    <md-table-cell>{{
                        item.name + "  第" + item.order + "便"
                      }}</md-table-cell>
                    <md-table-cell>
                      <md-button class="md-info" @click="editRouteData(index, 1)">編集</md-button>
                      <md-button class="md-danger" @click="deleteEditRoute(index)">削除</md-button>
                    </md-table-cell>
                  </md-table-row>
                </draggable>
              </md-table>
            </md-card-content>
          </md-card>
        </div>

        <Right>
          <md-button class="md-size-20" @click="editDataSwitch(-1), editReset()">編集取り消し</md-button>
          <md-button class="md-warning md-size-20" @click="editAdd(), editDataSwitch(-1), editReset()" :disabled="$v.editCourseName.$invalid">変更を保存</md-button>
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
    courses: {
      type: Object,
    },
    newCourse: {
      type: Array,
    },
  },
  data() {
    return {
      show: false, // 新規コース欄の表示フラグ
      courseName: null, //新規コース欄でコース名をバインドする変数
      course: [], // 新規コース欄で保存前のコース内容を保存しておく配列
      edit: null, // コース編集ページの表示フラグ
      editCourseName: null, // コース編集欄でコース名をバインド
      editCourse: [], // コース編集欄で作成中のコース一覧の乗法をバインド
    };
  },
  methods: {
    /**
     * 新規コース欄の表示フラグを切り替える関数
     */
    newerSwitch() {
      if (this.show == false) {
        this.show = true;
      } else {
        this.show = false;
      }
    },

    /**
     * コース編集欄の表示フラグを切り替える関数
     * false or indexの値を格納する
     * @param  {num} index 編集ボタンを押した際のv-forのindex
     */
    editDataSwitch(index) {
      if (this.edit == null) {
        this.edit = index;
        // setTimeout(this.goToEdit,100); うまく動かない
      } else {
        this.edit = null;
      }
    },

    /**
     * 編集ボタンを押した際に，コース編集欄の各項目に対して該当するコース情報を格納する関数
     * @param  {num} index 編集ボタンを押した際のv-forのindex
     */
    editData(index) {
      this.editCourseName = this.courses.courses[index].name;
      for (var i = 0; i < this.courses.courses[index].course.length; i++) {
        this.editCourse.push(this.courses.courses[index].course[i]);
      }
    },

    /**
     * コース編集欄でコースに路線を追加する関数
     * @param {num} index 編集欄の路線一覧のv-forのindex
     */
    addEditCourse(index) {
      this.editCourse.push({
        id: this.routes.routes[index].id,
        name: this.routes.routes[index].name,
      });
    },

    /**
     * 新規作成中のコース情報を初期化する関数
     */
    reset() {
      this.course = [];
    },

    /**
     * コース編集中のコース情報を初期化する関数
     */
    editReset() {
      this.editCourse = [];
    },

    /**
     * 親から受け取った情報から，作成するコース欄にデータを入れる関数
     * @param {Object} route 追加するコースの情報が詰まったObjectを親から取得
     * @param {Array} routeDetail バス停一つ一つのid,name,time,is_usedが入った開裂
     * @param {num} button 押下されたボタンの種類
     */
    addCourse(route, routeDetail, button, order) {
      if (button == 0) {
        this.course.push({
          id: route.id,
          name: route.name,
          order: order,
          route: routeDetail,
        });
      } else if (button == 1) {
        this.editCourse.push({
          id: route.id,
          name: route.name,
          order: order,
          route: routeDetail,
        });
      }
    },

    /**
     * 親から受け取った情報から，編集するコース欄にデータを入れる関数
     * @param {num} index
     * @param {Object} route  編集済みのデータ
     * @param {num} button ボタンの種類
     */
    addEditRoute(index, route, routeData, button, order) {
      if (button == 0) {
        this.course.splice(index, 1, {
          id: route.id,
          name: route.name,
          order: order,
          route: routeData,
        });
      } else {
        this.editCourse.splice(index, 1, {
          id: route.id,
          name: route.name,
          order: order,
          route: routeData,
        });
      }
    },

    /**
     * 新規コース情報を確定し，登録する関数
     */
    async add() {
      //APIを叩く処理
      const data = {
        name: this.courseName,
        course: this.course,
      };
      console.log(data);

      let url = "/web/course/register/";
      let result = await this.callPostAPI(url, data);
      this.notifyRegister(result.success);
      //更新処理
      this.updateAPI();
    },

    /**
     * コース編集の際の変更を確定し，登録する関数
     */
    async editAdd() {
      const data = {
        id: this.courses.courses[this.edit].id,
        name: this.editCourseName,
        course: this.editCourse,
      };
      let url = "/web/course/update/";
      let result = await this.callPostAPI(url, data);
      this.notifyUpdate(result.success);
      this.updateAPI();
    },

    /**
     * 新規コース作成中に，一度登録した路線を削除する関数
     * @param  {num} index v-forのindex
     */
    deleteRoute(index) {
      this.course.splice(index, 1);
    },

    /**
     * コース編集中に，一度登録した路線を削除する関数
     * @param  {num} index v-forのindex
     */
    deleteEditRoute(index) {
      this.editCourse.splice(index, 1);
    },

    /**
     * すでに作成済みのコースを削除する関数
     * @param  {num} index 削除するコースのid
     */
    async deleteCourse(index) {
      const data = {
        course_id: index,
      };

      let url = "/web/course/delete/";
      let result = await this.callPostAPI(url, data);
      this.notifyDelete(result.success);
      this.updateAPI();
    },

    /**
     * コース削除前のアラートを表示するための関数
     * @param  {[type]} index v-forのindex
     */
    onAlert(index) {
      let message = {
        title: "確認",
        body: "このコース情報を削除してもよろしいですか",
      };

      let options = {
        okText: "削除",
        cancelText: "キャンセル",
        backdropClose: true,
      };

      this.$dialog
        .confirm(message, options)
        .then(() => {
          this.deleteCourse(this.courses.courses[index].id);
        })
        .catch(function() {
          console.log("Cancel delete");
        });
    },

    /**
     * モーダル表示用の関数
     * @param  {num} index 親に該当するrouteIdを送るためにv-forのindexが必要
     * @param  {num} button 押下するボタンの種類
     */
    showModal(index, button) {
      var routeId = this.routes.routes[index].id;
      this.$emit("showModal", routeId, button);
    },

    /**
     * 編集用のモーダル表示
     * @param  {num} index  編集するコースのindex
     * @param  {num} button 新規作成(0)かコース編集(1)か
     */
    editRouteData(index, button) {
      var route = null;
      if (button == 0) {
        route = this.course[index];
      } else {
        console.log(button);
        console.log(index);
        route = this.editCourse[index];
      }
      this.$emit("showEditModal", index, route, button);
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
    courseName: {
      required,
    },
    editCourseName: {
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
