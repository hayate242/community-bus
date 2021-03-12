<template>
    <div class="content">
      <div class="md-layout">
        <div class="md-layout-item">
          <md-card>
            <md-card-header data-background-color="green">
              <h4 class="title">運賃管理</h4>
            </md-card-header>
            <md-card-content>
              <!-- 金額の編集ボタン -->
              <Right v-show="!editMode">
                <md-button
                  class="md-info md-layout-item md-size-20"
                  @click="editModeOn()"
                >
                  金額の編集
                </md-button>
              </Right>
              <Right v-show="editMode">
                <md-button
                  class="md-layout-item md-size-20"
                  @click="editCancel()"
                >
                  編集取り消し
                </md-button>
              </Right>

              <!-- 区分金額対応表 -->
              <md-card>
                <md-card-header data-background-color="green">
                  <h4 class="title">区分一覧</h4>
                </md-card-header>
                <md-card-content>
                  <div class="md-layout-item md-size-100">
                    <md-table>
                      <md-table-row>
                        <md-table-head>区分</md-table-head>
                        <md-table-head>
                          金額（円）
                        </md-table-head>
                      </md-table-row>

                      <md-table-row v-for="(item, index) in $v.items.$each.$iter" :key="item.type">
                        <!-- 区分 -->
                        <md-table-cell>{{ items[index].group }}</md-table-cell>
                        <!-- 金額 -->
                        <md-table-cell v-show="!editMode">{{ item.amount.$model | numberWithDelimiter }}</md-table-cell>
                        <md-table-cell v-show="editMode">
                          <span class="error" v-show="!item.amount.required">必須項目です</span>
                          <span class="error" v-show="!item.amount.numeric">数字のみご入力ください</span>
                          <md-field>
                            <md-input v-model.trim="item.amount.$model"></md-input>
                          </md-field>
                        </md-table-cell>
                      </md-table-row>
                    </md-table>
                  </div>
                </md-card-content>
              </md-card>
              <Right v-show="editMode">
                <md-button
                  class="md-warning md-size-20"
                  @click="editTerminate()"
                  :disabled="$v.items.$invalid"
                >
                  編集完了
                </md-button>
              </Right>
            </md-card-content>
          </md-card>
        </div>
      </div>
    </div>
</template>
<script>
import {
  required,
  numeric
} from "vuelidate/lib/validators";
import axios from "axios";
export default {
  data() {
    return {
      editMode: false,
      url: "/web/fare/",
      items: null,
      backup: null
    };
  },
  methods: {
    editModeOn() {
        this.editMode = true;
        this.backup = JSON.parse(JSON.stringify(this.items));
    },
    editTerminate() {
        this.callPostAPI(this.url + "create/", this.items)
        .then(result => {
            this.getItem()
            this.notifyUpdate(result.success)
        })
        this.editMode = false;
    },
    editCancel() {
        this.editMode = false;
        this.items = JSON.parse(JSON.stringify(this.backup));
    },
    getItem() {
        this.callGetAPI(this.url, "")
        .then(result => this.items = result ? result : [])
    }
  },
  filters: {
    numberWithDelimiter(value) {
        return value.toString().replace(/(\d)(?=(\d{3})+$)/g, '$1,')
    }
  },
  created() {
      this.getItem()
  },
  validations: {
    items: {
      required,
      $each: {
        amount: {
            required,
            numeric
        }
      }
    }
  }
};
</script>
<style>
.md-table-cell:last-child .md-table-cell-container {
    flex-direction: column;
    align-items: flex-start;
}
</style>
<style scoped>
.md-field {
    margin: 0;
    padding-top: 0px;
    min-height: 0px;
}
</style>
