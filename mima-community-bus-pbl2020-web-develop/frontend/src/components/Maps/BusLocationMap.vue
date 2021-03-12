<template>
<div>
  <md-card>
    <md-card-header data-background-color="orange">
      <h4 class="title">バスの現在位置</h4>
    </md-card-header>
    <md-card-content>
      <div id="map" v-bind:style="mapStyles"></div>
      <course-bar :routes="routes"> </course-bar>
    </md-card-content>
  </md-card>
</div>
</template>

<script>
import {
  API_KEY
} from "./API_KEY";
import {
  Loader,
  LoaderOptions
} from "google-maps";

import CourseBar from "./CourseBar.vue";
import store from "@/store.js";

const loader = new Loader(API_KEY);
export default {
  components: {
    CourseBar,
  },
  props: {
    mapStyles: {
      type: Object,
      default: () => ({
        "max-height": "500px",
      }),
    },
  },
  name: "bus-location-map",
  data() {
    return {
      google: null,
      intervalId: undefined,
      routeColors: [{
          name: "blue",
          color: "#0328fc"
        },
        {
          name: "orange",
          color: "#F5AF25"
        },
        {
          name: "pink",
          color: "#FF82A3"
        },
        {
          name: "green",
          color: "#65D41C"
        },
        {
          name: "purple",
          color: "#A337FF"
        },
        {
          name: "cyan",
          color: "#2AD7EB"
        },
      ],
      map: null,
      mapLocation: {
        lat: 33.29554,
        lng: 132.618783
      }, //33.295540, 132.618783
      mapCenter: null,
      busLocationApiUrl: "/web/map/location/bus/",
      routeLocationsApiUrl: "/web/map/location/route/",
      buses: {},
      routeLocations: {},
      routes: [],
      busMarkers: [],
    };
  },
  async mounted() {
    this.google = await loader.load();
    this.initBusLocationMap();
    this.initCourse();
    this.initBus();
    // interval job
    this.intervalId = setInterval(this.intervalJobs, 5000);
  },
  beforeDestroy() {
    clearInterval(this.intervalId); // clear interval
  },
  methods: {
    async initBus() {
      await this.getBusLocation();
      this.setBusLocations();
    },
    async initCourse() {
      await this.getRouteLocations();
      this.drawCourse();
      this.setRoutesArray();
    },
    initBusLocationMap: function() {
      this.mapCenter = new this.google.maps.LatLng(
        this.mapLocation["lat"],
        this.mapLocation["lng"]
      );
      var mapOptions = {
        zoom: 14,
        center: this.mapCenter,
        scrollwheel: false, // we disable de scroll over the map, it is a really annoing when you scroll through page
      };
      this.map = new this.google.maps.Map(
        document.getElementById("map"),
        mapOptions
      );
    },
    setRoute: function(points, routeColor, drowIndex) {
      // 経路情報に変更がある場合は，storeの情報をクリアする
      if (JSON.stringify(Object.entries(store.getters.route_locations)) != JSON.stringify(Object.entries(this.routeLocations))) {
        store.commit("path_clear");
      }

      const that = this;
      loader.load().then(function(google) {
        if (store.getters.path_data.length == 0) {
          // 地点を分割してルート検索を行います。
          var d = new google.maps.DirectionsService(); // ルート検索オブジェクト
          var origin = null,
            waypoints = [],
            dest = null; // 出発地、経由地、目的地
          var resultMap = {}; // 分割してルート検索した結果データ
          var requestIndex = 0; // 検索番号
          var done = 0; // ルート検索が完了した数
          for (var i = 0, len = points.length; i < len; i++) {
            // 最初の場合、originに値をセット
            if (origin == null) {
              origin = points[i];
            }
            // 経由地が25たまったか最後の地点の場合、ルート検索
            else if (waypoints.length == 25 || i == len - 1) {
              dest = points[i];

              (function(index) {
                // ルート検索の条件
                var request = {
                  origin: origin, // 出発地
                  destination: dest, // 目的地
                  waypoints: waypoints, // 経由地
                  travelMode: google.maps.DirectionsTravelMode.DRIVING, // 交通手段(歩行。DRIVINGの場合は車)
                };
                // console.log(request);
                // ルート検索
                d.route(request, function(result, status) {
                  // OKの場合ルートデータ保持
                  if (status == google.maps.DirectionsStatus.OK) {
                    resultMap[index] = result; // 並行でリクエストするので配列だとリクエスト順とずれる場合があります
                    done++;
                  } else {
                    console.log(status); // デバッグ
                    // Todo ZERO_RESULTSだった時の対応
                  }
                });
              })(requestIndex);

              requestIndex++;
              origin = points[i]; // 今回の目的地を次回の出発地にします。
              waypoints = [];
            }
            // 上記以外、waypointsに地点を追加
            else {
              waypoints.push({
                location: points[i],
                stopover: true
              });
            }
          }

          var sid = setInterval(function() {
            // 分割したすべての検索が完了するまで待ちます。
            if (requestIndex > done) return;
            clearInterval(sid);

            // すべての結果のルート座標を順番に取得して平坦な配列にします。
            var path = [];
            var result;
            for (var i = 0, len = requestIndex; i < len; i++) {
              result = resultMap[i]; // 検索結果
              // console.log(result);
              var legs = result.routes[0].legs; // Array<DirectionsLeg>
              for (var li = 0, llen = legs.length; li < llen; li++) {
                var leg = legs[li]; // DirectionLeg
                var steps = leg.steps; // Array<DirectionsStep>
                // DirectionsStepが持っているpathを取得して平坦(2次元配列→1次元配列)にします。
                var _path = steps
                  .map(function(step) {
                    return step.path;
                  })
                  .reduce(function(all, paths) {
                    return all.concat(paths);
                  });
                path = path.concat(_path);
                // マーカーが必要ならマーカーを表示します。
                // that.setBusStops(leg.start_location, leg.start_address);
              }
            }
            // pathの内容をstoreに保存
            store.commit({
              type: "path",
              path_data: path,
              route_locations: that.routeLocations,
            })

            // マーカーが必要ならマーカーを表示します。(最終)
            // var endLeg = result.routes[0].legs[result.routes[0].legs.length - 1];
            // that.setBusStops(endLeg.end_location, endLeg.end_address);

            // google mapの経路検索APIからパスを描画します。
            var line = new google.maps.Polyline({
              map: that.map, // 描画先の地図
              strokeColor: routeColor, // 線の色
              strokeOpacity: 0.8, // 線の不透明度
              strokeWeight: 2, // 先の太さ
              path: path, // 描画するパスデータ
            });
          }, 1000);
        } else {
          // storeの情報からパスを描画します。
          var path_data = store.getters.path_data;
          var line = new google.maps.Polyline({
            map: that.map, // 描画先の地図
            strokeColor: routeColor, // 線の色
            strokeOpacity: 0.8, // 線の不透明度
            strokeWeight: 2, // 先の太さ
            path: path_data[drowIndex], // 描画するパスデータ
          });
        }
      });
    },
    setBusStops: function(position, content, is_passing_point) {
      // マーカーを表示する場合の準備
      var infoWindow = new this.google.maps.InfoWindow();
      var marker = new this.google.maps.Marker({
        map: this.map, // 描画先の地図
        position: position, // 座標
        icon: {
          url: require("@/assets/img/bus_stop.png"),
          scaledSize: new this.google.maps.Size(30, 30),
        },
      });
      // クリック時吹き出しを表示
      marker.addListener("click", function() {
        infoWindow.setContent(content);
        infoWindow.open(map, marker);
      });
      if (is_passing_point == true) {
        marker.visible = false
      }
    },
    /**
     * Google Map上にバスの追加
     */
    setBusLocations: function() {
      for (var key in this.buses) {
        // reset marker
        if (typeof this.busMarkers[key] !== "undefined") {
          this.busMarkers[key].setMap(null);
        }
        // location
        const location = new this.google.maps.LatLng(
          this.buses[key]["latitude"],
          this.buses[key]["longitude"]
        );

        this.busMarkers[key] = new this.google.maps.Marker({
          map: this.map,
          position: location,
          title: "Bus",
          icon: {
            url: this.buses[key]["translucent_flg"] == 0 ? require("@/assets/img/bus_icon" + key + ".png") : require("@/assets/img/bus_icon_translucent" + key + ".png"),
            scaledSize: new this.google.maps.Size(60, 60),
          },
        })
        this.addMarkerInfo(
          this.busMarkers[key],
          this.busInfoText(this.buses[key])
        );
        // To add the marker to the map, call setMap();
        this.busMarkers[key].setMap(this.map);
      }
    },
    addMarkerInfo: function(marker, content) {
      new this.google.maps.InfoWindow({
        content,
        disableAutoPan: true
      }).open(
        marker.getMap(),
        marker
      );
      this.google.maps.event.addListener(marker, "click", function(event) {
        new this.google.maps.InfoWindow({
          content
        }).open(
          marker.getMap(),
          marker
        );
      });
    },
    busInfoText: function(bus) {
      return (
        bus["route_name"] +
        "<br>" +
        "空き：" +
        String(bus["vacancy_num"]) +
        "<br>" +
        // "遅れ：" +
        // bus["delay"] +
        // "<br>" +
        ((bus["next_bus_stop_name"] != "") ?
          "次のバス停：" + bus["next_bus_stop_name"] + "<br>" :
          "")
      );
    },
    drawCourse: function() {
      const that = this;
      const routeLatLng = this.routeLocations.routes.map((route) => {
        return route.bus_stops.map((bus_stop) => {
          return new this.google.maps.LatLng(
            bus_stop["latitude"],
            bus_stop["longitude"]
          );
        });
      });
      // コースの表示
      var points = [];
      var index = 0;
      const color_len = that.routeColors.length;
      routeLatLng.forEach(function(latlangs) {
        points = points.concat(latlangs);
        that.setRoute(points, that.routeColors[index % color_len]["color"], index);
        points = [];
        index++;
      });
      // バス停の表示
      this.routeLocations.routes.forEach(function(route) {
        route.bus_stops.forEach(function(bus_stop) {
          that.setBusStops(
            new that.google.maps.LatLng(
              bus_stop["latitude"],
              bus_stop["longitude"]
            ),
            `${bus_stop.bus_stop_name}`,
            bus_stop.is_passing_point
          );
        });
      });
    },
    setRoutesArray: function() {
      const that = this;
      var index = 0;
      const color_len = that.routeColors.length;
      this.routeLocations.routes.forEach(function(route) {
        that.routes.push({
          route_name: route.route_name,
          style: {
            background: `linear-gradient(transparent 80%, ${
              that.routeColors[index % color_len]["color"]
            } 30%)`,
          },
        });
        index++;
      });
    },
    async getBusLocation() {
      const buses = await this.callGetAPI(this.busLocationApiUrl, "", false);
      this.buses = buses.bus_locations;
    },
    async getRouteLocations() {
      this.routeLocations = await this.callGetAPI(
        this.routeLocationsApiUrl,
        "",
        false
      );
    },
    intervalJobs: function() {
      this.initBus();
    },
  },
};
</script>
