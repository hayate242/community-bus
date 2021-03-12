<template>
<div>
  <md-field v-if="selectDate">
    <VueCtkDateTimePicker v-model="date" label="日付を選択してください" format="YYYY-MM-DD" formatted="YYYY-MM-DD" overlay only-date />
  </md-field>
  <md-field v-if="selectDate" class="mt-n13">
    <label>コースを選択</label>
    <md-select v-model="selectedCourse">
      <md-option v-for="course in courses" :key="course.course_id" :value="course.course_id">{{ course.course_name }}</md-option>
    </md-select>
  </md-field>
  <p v-if="items.length">データがありません</p>
  <md-card>
    <md-card-header data-background-color="green">
      <h4 class="title">運行状況一覧</h4>
    </md-card-header>

    <md-card-content>
      <div v-if="selectDate" class="md-layout-item md-size-100">
        <md-table>
          <md-table-row>
            <md-table-head>バス番号</md-table-head>
            <md-table-head>路線名</md-table-head>
            <md-table-head>バス停名</md-table-head>
            <md-table-head>予定時刻</md-table-head>
            <md-table-head>到着時刻</md-table-head>
            <md-table-head>運行状況</md-table-head>
          </md-table-row>

          <md-table-row v-for="(item, i) in items.bus_record" :key="i">
            <md-table-cell v-if="item.course_id == selectedCourse">{{item.bus_id}}号車</md-table-cell>
            <md-table-cell v-if="item.course_id == selectedCourse">{{ item.bus_route }}</md-table-cell>
            <md-table-cell v-if="item.course_id == selectedCourse">{{ item.bus_stop }}</md-table-cell>
            <md-table-cell v-if="item.course_id == selectedCourse">{{ item.estimated_time }}</md-table-cell>
            <md-table-cell v-if="item.course_id == selectedCourse">{{ item.arrival_time }}</md-table-cell>
            <md-table-cell v-if="item.course_id == selectedCourse"><span v-html="diff(item.estimated_time, item.arrival_time)"></span></md-table-cell>
          </md-table-row>
        </md-table>
      </div>
      <div v-else class="md-layout-item md-size-100">
        <md-table>
          <md-table-row>
            <md-table-head>バス番号</md-table-head>
            <md-table-head>路線名</md-table-head>
            <md-table-head>バス停名</md-table-head>
            <md-table-head>予定時刻</md-table-head>
            <md-table-head>到着時刻</md-table-head>
            <md-table-head>運行状況</md-table-head>
          </md-table-row>

          <md-table-row v-for="(item, i) in items.bus_record" :key="i">
            <md-table-cell>{{item.bus_id}}号車</md-table-cell>
            <md-table-cell>{{ item.bus_route }}</md-table-cell>
            <md-table-cell>{{ item.bus_stop }}</md-table-cell>
            <md-table-cell>{{ item.estimated_time }}</md-table-cell>
            <md-table-cell>{{ item.arrival_time }}</md-table-cell>
            <md-table-cell><span v-html="diff(item.estimated_time, item.arrival_time)"></span></md-table-cell>
          </md-table-row>
        </md-table>
      </div>

    </md-card-content>
  </md-card>
</div>
</template>
<script>
export default {
  props: {
    selectDate: {},
  },
  data() {
    return {
      courseListApiUrl: "/bus/course/",
      date: null,
      selectedCourse: 1,
      items: [],
      courses: [],
    };
  },
  methods: {
    /**
     * コース一覧の取得
     */
    async setCourses() {
      const courses = await this.callGetAPI(this.courseListApiUrl, "");
      console.log(courses)
      this.courses = courses.Courses;
      this.selectedCourse = this.courses[0].course_id;
    },
    diff(estimatedTime, arrivalTime) {
      var estTime = new Date("2000/1/1 " + estimatedTime);
      var arrTime = new Date("2000/1/1 " + arrivalTime);
      var diff = (arrTime.getTime() - estTime.getTime()) / (1000 * 60);
      if (diff > 0) {
        if (diff >= 5) {
          return "<span style='color:red'>" + diff + "分遅延" + "</span>";
        } else {
          return "<span style='color:black'>" + diff + "分遅延" + "</span>";
        }
      } else if (diff < 0) {
        if (diff <= -5) {
          return (
            "<span style='color:#ed8002'>" + // orange
            -1 * diff +
            "分早い" +
            "</span>"
          );
        } else {
          return (
            "<span style='color:black'>" + -1 * diff + "分早い" + "</span>"
          );
        }
      } else {
        return "<span style='color:black'> 定刻 </span>";
      }
    },
    /**
     * 乗降記録の一覧を取得
     */
    async getBusHistory() {
      const url = "/web/bus/history/";
      const params = {
        date: this.date,
        selectDate: (this.selectDate) ? true : false
      };
      const items = await this.callPostAPI(url, params);
      this.items = items;
    },
  },
  mounted: function() {
    let date = new Date(); //new演算子でオブジェクトのインスタンスを生成
    //現在時刻の取得 **ここからはjavascript**
    this.date =
      date.getFullYear() +
      "-" +
      parseInt(date.getMonth() + 1, 10) +
      "-" +
      date.getDate();

    // コース一覧取得
    this.setCourses();
    this.getBusHistory();
    this.intervalId = setInterval(this.getBusHistory, 5000);
  },
  watch: {
    date: async function() {
      this.getBusHistory();
    },
    selectedCourse: async function() {
      this.getBusHistory();
    },
  },
};
</script>
