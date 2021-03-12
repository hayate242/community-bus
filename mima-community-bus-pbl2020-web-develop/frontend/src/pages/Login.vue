<template>
  <div class="centered-container">
    <md-content class="md-elevation-3">
      <div class="title">
        <div class="md-title">みまっぷ管理画面ログイン</div>
      </div>

      <div class="form">
        <span class="validation" v-if="!$v.email.required && $v.email.$dirty"
          >必須項目です</span
        >
        <span class="validation" v-if="!$v.email.email && $v.email.$dirty"
          >正しいメールアドレスを入力してください</span
        >
        <md-field>
          <label>メールアドレス</label>
          <md-input
            v-model="email"
            @blur="$v.email.$touch()"
            autofocus
          ></md-input>
        </md-field>

        <span class="validation" v-if="$v.pass.$invalid && $v.pass.$dirty"
          >必須項目です</span
        >
        <md-field md-has-password>
          <label>パスワード</label>
          <md-input
            v-model="pass"
            type="password"
            @blur="$v.pass.$touch()"
          ></md-input>
        </md-field>
      </div>

      <!-- エラーメッセージ表示領域 -->
      <div v-if="error == true" class="error">
        <p>ログイン認証に失敗しました．</p>
        <p>もう一度試してください．</p>
      </div>
      <!-- トークン有効期限切れの処理 -->
      <div class="error">
        <p v-html="message"></p>
      </div>

      <div class="actions md-layout md-alignment-center">
        <md-button
          class="md-raised md-primary"
          @click="auth"
          :disabled="$v.$invalid"
          >ログイン</md-button
        >
      </div>
    </md-content>
  </div>
</template>

<script>
import { required, email } from "vuelidate/lib/validators";
export default {
  props: {
    message: { type: String },
  },
  data() {
    return {
      email: null,
      pass: null,
      error: false,
    };
  },
  methods: {
    /**
     * エラー表示の表示非表示を切り替える
     */
    errorSwitch() {
      if (this.error == false) {
        this.error = true;
      } else {
        this.error = false;
      }
    },

    /**
     * ログイン用のAPIを叩いて，トークンとユーザーid，ユーザー名を取得して，管理画面トップにリダイレクト
     */
    async auth() {
      //エラー表示がされていれば，非表示にする
      if (this.error == true) {
        this.errorSwitch();
      }

      //ログイン成功時の処理
      const result = await this.login(this.email, this.pass);
      if (result == true) {
        //管理画面トップにリダイレクト
        this.$router.push("/admin/dashboard");
      }
      //ログイン失敗時の処理
      else {
        //エラーメッセージを表示
        if (this.error == false) {
          this.errorSwitch();
        }
      }
    },
  },
  watch: {
    email: function () {
      this.message = "";
    },
    pass: function () {
      this.message = "";
    },
  },
  validations: {
    email: {
      required,
      email,
    },
    pass: {
      required,
    },
  },
};
</script>

<style lang="scss">
.centered-container {
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  height: 100vh;
  .title {
    text-align: center;
    margin-bottom: 30px;
    img {
      margin-bottom: 16px;
      max-width: 80px;
    }
  }
  .actions {
    .md-button {
      margin: 0;
    }
  }
  .form {
    margin-bottom: 60px;
  }
  .md-content {
    z-index: 1;
    padding: 40px;
    width: 100%;
    max-width: 400px;
    position: relative;
  }
  .loading-overlay {
    z-index: 10;
    top: 0;
    left: 0;
    right: 0;
    position: absolute;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.9);
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .error {
    text-align: center;
    color: #ff0000;
  }
  .validation {
    color: #8a0421;
    border-color: #dd0f3b;
    background-color: #ffd9d9;
  }
}
</style>
