<template>
  <div class="here-map">
    <div ref="map" v-bind:style="{ width: width, height: height }"></div>
    <button class="backHome" @click="getStart">Current position </button>
  </div>
</template>

<script>
import { constants } from 'fs';
export default {
  name: "HereMap",
  data() {
    return {
      curPos: {},
      map: {},
      platform: {},
      location: {},
      containers: {},
      geoLoc: {},
      firstTime: false
    };
  },
  props: {
    appId: String,
    appCode: String,
    width: String,
    height: String,
    show: Boolean
  },
  created() {
    this.platform = new H.service.Platform({
      app_id: this.appId,
      app_code: this.appCode
    });
  },
  watch: {
    show(x) {
      if (x) { 
        this.firstTime = true
        return this.updatePosition() 
      }
      else { 
        navigator.geolocation.clearWatch(this.geoLoc)
        this.firstTime = false
      }
    }
  },
  methods: {
    createMap() {
      this.platform = new H.service.Platform({
        app_id: this.appId,
        app_code: this.appCode
      });
      var layers = this.platform.createDefaultLayers();
      this.map = new H.Map(this.$refs.map, layers.normal.map, {
        center: { lat: 50.0834188, lng: 14.4041256 },
        zoom: 13
      });
      var events = new H.mapevents.MapEvents(this.map);
      var behavior = new H.mapevents.Behavior(events);
      if (this.show) {
        this.firstTime = true
        return this.updatePosition 
      }
    },
    updatePosition() {
      let me = null
      this.geoLoc = navigator.geolocation.watchPosition(cord => {
        console.log(cord);
        this.curPos = {lat:cord.coords.latitude,lng:cord.coords.longitude};
        let svgMarkup = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zm0-5C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
        let icon = new H.map.Icon(svgMarkup)
        let coords = this.curPos
        if (me) { this.map.removeObject(me) }
        me = new H.map.Marker(coords, {icon: icon});
        this.map.addObject(me);
        if (this.show && this.firstTime) {
          this.axios({
            url:'http://localhost:5000/get-containers',
            method: 'get',
            params: {
              lat: this.$route.query.lat,
              lng: this.$route.query.lng,
              containers:this.$route.query.containers
            }
          }).then((data)=>{
            this.containers = data.data.data;
            // console.log(containers);
            for(let i = 0; i < this.containers.length;i++){
              let marker = new H.map.Marker({lat:this.containers[i].coordinates[0], lng:this.containers[i].coordinates[1]});
              this.map.addObject(marker);
            }
            }).catch((err)=>{console.log('error occured',err)})
          this.map.setCenter({
            lat: cord.coords.latitude,
            lng: cord.coords.longitude
          });
          this.map.setZoom(17);
          this.firstTime = true
        }
      }, err => {
        console.log(err)
        return
      },{
        enableHighAccuracy : true,
        timeout : 60000,
        maximumAge : 0
      });
    },
    getStart() {
      this.map.setCenter(this.curPos)
      this.map.setZoom(19)
    }
  },
  mounted() {
    this.createMap()
  }
};
</script>

<style scoped>
.here-map {
  display: flex;
  height: 100%;
  width: 100%;
}

.backHome {
  position: absolute;
  left: 50%;
  bottom: 30px;
  transform: translateX(-50%);
  white-space: nowrap;
  background: rgb(15, 172, 112);
  padding: 10px 25px;
  border-radius: 50px;
  font-weight: bold;
  font-size: 1.3em;
  align-self: flex-start;
  margin: auto;
  color: white;
}

</style>
