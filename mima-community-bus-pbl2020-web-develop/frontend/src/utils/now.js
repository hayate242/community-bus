export default {
  methods: {
    nowDate() {
      let date = new Date();
      let now =
        date.getFullYear() +
        "-" +
        parseInt(date.getMonth() + 1, 10) +
        "-" +
        date.getDate();
      return now;
    },
    oneMonthsAgoDate() {
      let date = new Date();
      date.setMonth(date.getMonth() - 1);
      let oneMonthsAgo =
        date.getFullYear() +
        "-" +
        parseInt(date.getMonth() + 1, 10) +
        "-" +
        date.getDate();
      return oneMonthsAgo;
    },
    nowDateTime() {
      let date = new Date();
      let now =
        date.getFullYear() +
        "-" +
        parseInt(date.getMonth() + 1, 10) +
        "-" +
        date.getDate();
      +" " +
        date.getHours() +
        ":" +
        date.getMinutes() +
        ":" +
        date.getSeconds();
      return now;
    }
  }
};
