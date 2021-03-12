<template>
  <div>
    <md-table v-model="users" :table-header-color="tableHeaderColor">
      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="バス停名">{{ item.name }}</md-table-cell>
        <md-table-cell md-label="予定時刻">{{
          item.estimated_time
        }}</md-table-cell>
        <md-table-cell md-label="到着時刻">{{
          item.arrival_time
        }}</md-table-cell>
        <md-table-cell md-label="遅延状況">{{ item.delay }}</md-table-cell>
      </md-table-row>
    </md-table>
  </div>
</template>

<script>
export default {
  name: "course-table",
  props: {
    tableHeaderColor: {
      type: String,
      default: ""
    },
    courseId: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      selected: [],
      users: [
        {
          name: "三間支所",
          estimated_time: "11:00",
          arrival_time: "11:05",
          delay: "5分遅延"
        },
        {
          name: "小池",
          estimated_time: "11:10",
          arrival_time: "11:10",
          delay: "定刻"
        }
      ]
    };
  }
};
</script>
