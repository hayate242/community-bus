<template>
<div class="content">
  <div class="md-layout">
    <div class="md-layout-item">
      <md-card>
        <md-card-header data-background-color="green">
          <h4 class="title">システムユーザー管理</h4>
        </md-card-header>
        <md-card-content>
          <!-- 新規ユーザーボタン -->
          <Right v-if="show == false">
            <md-button class="md-info md-layout-item md-size-20" @click="newUserSwitch()">新規ユーザー登録</md-button>
          </Right>

          <!-- 新規ユーザー情報入力欄 -->
          <div v-if="this.show == true">
            <md-card>
              <md-card-header data-background-color="blue">
                <h4 class="title">新規ユーザー登録</h4>
              </md-card-header>
              <md-card-content>
                <span class="error" v-if="$v.name.$invalid && $v.name.$dirty">必須項目です</span>
                <md-field>
                  <label>ユーザー名</label>
                  <md-input v-model="name" @blur="$v.name.$touch()"></md-input>
                </md-field>

                <span class="error" v-if="!$v.email.required && $v.email.$dirty">必須項目です</span>
                <span class="error" v-if="!$v.email.email && $v.email.$dirty">正しいメールアドレスを入力してください</span>
                <md-field>
                  <label>メールアドレス</label>
                  <md-input v-model="email" @blur="$v.email.$touch()"></md-input>
                </md-field>

                <span class="error" v-if="$v.password.$invalid && $v.password.$dirty">必須項目です</span>
                <md-field>
                  <label>パスワード</label>
                  <md-input type="password" v-model="password" @blur="$v.password.$touch()"></md-input>
                </md-field>

                <span class="error" v-if="$v.groupId.$invalid && $v.groupId.$dirty">必須項目です</span>
                <md-field class="mt-n13">
                  <label>アカウント区分</label>
                  <md-select v-model="groupId">
                    <md-option v-for="(group, index) in groups" :key="index" :value="group.id" @blur="$v.groupId.$touch()">
                      {{ group.name }}
                    </md-option>
                  </md-select>
                </md-field>

                <Right>
                  <md-button class="md-size-20" @click="newUserSwitch(), reset()">登録取り消し</md-button>
                  <md-button class="md-warning md-size-20" @click="newUserSwitch(), registerUser(), reset()" :disabled="
                        $v.name.$invalid ||
                        $v.email.$invalid ||
                        $v.password.$invalid ||
                        $v.groupId.$invalid
                      ">登録確定</md-button>
                </Right>
              </md-card-content>
            </md-card>
          </div>

          <!-- ユーザー情報テーブル -->
          <md-card>
            <md-card-header data-background-color="green">
              <h4 class="title">ユーザー一覧</h4>
            </md-card-header>
            <md-card-content>
              <div class="md-layout-item md-size-100">
                <md-table v-model="items">
                  <md-table-row>
                    <md-table-head>ユーザー名</md-table-head>
                    <md-table-head>メールアドレス</md-table-head>
                    <md-table-head>アカウント区分</md-table-head>
                    <md-table-head>編集</md-table-head>
                    <md-table-head>削除</md-table-head>
                  </md-table-row>

                  <md-table-row v-for="(item, index) in items.users" :key="item.id">
                    <md-table-cell>{{ item.name }}</md-table-cell>
                    <md-table-cell>{{ item.email }}</md-table-cell>
                    <md-table-cell>{{getAccountCategoryName(item.user_group_id)}}</md-table-cell>
                    <md-table-cell>
                      <div v-if="edit == null">
                        <md-button class="md-info" @click="editDataSwitch(index), editData(index)">編集</md-button>
                      </div>
                      <div v-else>
                        <md-button class="md-info" @click="editDataSwitch(index), editData(index)" disabled>編集</md-button>
                      </div>
                    </md-table-cell>
                    <md-table-cell>
                      <div v-if="edit != null">
                        <md-button class="md-danger" @click="onAlert(index)" disabled>削除</md-button>
                      </div>
                      <div v-else>
                        <md-button class="md-danger" @click="onAlert(index)" :disabled="isLoginUser(item.id)">削除</md-button>
                      </div>
                    </md-table-cell>
                  </md-table-row>
                </md-table>
              </div>
            </md-card-content>
          </md-card>

          <!-- 編集時情報欄 -->
          <div v-if="edit != null" id="edit">
            <md-card>
              <md-card-header data-background-color="blue">
                <h4 class="title">運転手編集</h4>
              </md-card-header>
              <md-card-content>
                <span class="error" v-if="$v.editName.$invalid && $v.editName.$dirty">必須項目です</span>
                <md-field>
                  <label>運転手名</label>
                  <md-input v-model="editName" @blur="$v.editName.$touch()"></md-input>
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

                <span class="error" v-if="!$v.editGroupId.required && $v.editGroupId.$dirty">必須項目です</span>
                <md-field class="mt-n13">
                  <label>アカウント区分</label>
                  <md-select v-model="editGroupId">
                    <md-option v-for="(group, index) in groups" :key="index" :value="group.id" @blur="$v.editGroupId.$touch">
                      {{ group.name }}
                    </md-option>
                  </md-select>
                </md-field>

                <Right>
                  <md-button class="md-size-20" @click="editDataSwitch(-1), reset()">編集取り消し</md-button>
                  <md-button class="md-warning md-size-20" @click="editUser(), editDataSwitch(-1), reset()" :disabled="$v.editName.$invalid || $v.editEmail.$invalid">変更を保存</md-button>
                </Right>
              </md-card-content>
            </md-card>
          </div>
        </md-card-content>
      </md-card>
    </div>
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
      items: {
        users: [],
      },
      userUrl: "/web/user/",
      userRegisterUrl: "/web/user/register/",
      userEditUrl: "/web/user/update/",
      userDeleteUrl: "/web/user/delete/",
      edit: null,
      name: null,
      email: null,
      groupId: null,
      password: null,
      editName: null,
      editEmail: null,
      editPassword: null,
      editGroupId: null,
      groups: [{
          id: 1,
          name: "宇和島市職員",
        },
        {
          id: 2,
          name: "委託バス会社職員",
        }
      ],
    };
  },
  methods: {
    /**
     * アカウント区分名をアカウント区分idから取得する関数
     * @param  {[type]} id アカウント区分のid
     * @return {[type]} アカウント区分名
     */
    getAccountCategoryName(id) {
      var name = this.groups.filter(function(item) {
        if (item.id == id) return true;
      })
      return name[0].name
    },

    isLoginUser(userId) {
      return this.$store.state.userId == userId ? true : false;
    },
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
    editData(index) {
      this.editName = this.items.users[index].name;
      this.editEmail = this.items.users[index].email;
      this.editPassword = "";
      this.editGroupId = this.items.users[index].user_group_id;
    },
    reset() {
      this.name = null;
      this.email = null;
      this.password = "";
      this.editGroupId = null;
    },
    /**
     * 編集
     */
    async editUser(user_id) {
      const user = {
        id: this.items.users[this.edit].id,
        user_name: this.editName,
        email: this.editEmail,
        password: this.editPassword,
        user_group_id: this.editGroupId,
      };
      const result = await this.callPostAPI(this.userEditUrl, user);
      if ("message" in result) {
        this.notifyUpdate(result.success, result.message);
      } else {
        this.notifyUpdate(result.success);
      }
      if (result.success) {
        this.getUsers();
      }
    },
    async deleteItem(id) {
      const user = {
        id,
      };
      const result = await this.callPostAPI(this.userDeleteUrl, user);
      if (result.success) {
        this.notifyPanel(
          "<p>ユーザーを削除しました.</p>",
          "info",
          "top",
          "left"
        );
        this.getUsers();
      } else {
        this.notifyPanel(
          "<p>ユーザーの削除に失敗しました.</p>",
          "danger",
          "top",
          "left"
        );
      }
    },
    onAlert(index) {
      let message = {
        title: "確認",
        body: "このユーザーの情報を削除してもよろしいですか",
      };

      let options = {
        okText: "削除",
        cancelText: "キャンセル",
        backdropClose: true,
      };

      this.$dialog
        .confirm(message, options)
        .then(() => {
          this.deleteItem(this.items.users[index].id);
        })
        .catch(function() {
          console.log("Cancel delete");
        });
    },
    /**
     * ユーザー一覧の取得
     */
    async getUsers() {
      this.items = await this.callGetAPI(this.userUrl, "");
    },
    /**
     * ユーザーの登録
     */
    async registerUser() {
      const user = {
        user_name: this.name,
        email: this.email,
        password: this.password,
        user_group_id: this.groupId,
      };
      const result = await this.callPostAPI(this.userRegisterUrl, user);
      if ("message" in result) {
        this.notifyRegister(result.success, result.message);
      } else {
        this.notifyRegister(result.success);
      }
      if (result.success) {
        this.getUsers();
      }
    },
  },
  mounted() {
    this.getUsers();
  },
  validations: {
    name: {
      required,
    },
    email: {
      required,
      email,
    },
    password: {
      required,
    },
    groupId: {
      required,
    },
    editName: {
      required,
    },
    editEmail: {
      required,
      email,
    },
    editGroupId: {
      required,
    },
  },
};
</script>
<style></style>
