<template>
  <div class="here-map">
    <div ref="map" v-bind:style="{ width: width, height: height }"></div>
    <button class="backHome" @click="getStart">Current position</button>
  </div>
</template>

<script>
import { generateMarkerBlob } from '../generateMarkerBlob.js';
import { constants } from 'fs';
export default {
  name: "HereMap",
  data() {
    return {
      curPos: {},
      map: {},
      ui: null,
      platform: {},
      location: {},
      containers: {},
      firstTime: null,
      markers: null,
      svgMarker: '',
      svgLocationMarker: '',
      geoLoc: {},
      firstTime: false
    };
  },
  props: {
    appId: String,
    appCode: String,
    width: String,
    height: String,
    show: Boolean,
    public: Boolean
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
      this.ui = H.ui.UI.createDefault(this.map,layers);
      var events = new H.mapevents.MapEvents(this.map);
      var behavior = new H.mapevents.Behavior(events);
      if (this.show) {
        this.firstTime = true
        return this.updatePosition 
      }
      this.markers = new H.map.Group();
      this.map.addObject(this.markers);

      this.markers.addEventListener(
        "tap",
        this.addBubble,
        false
      );
    },
    loadSVG(url) {
      fetch('/container-blank.svg').then(data => data.text()).then(text => {this.svgMarker = new H.map.Icon(text);console.log('created svg marker')});
      fetch('/location-point.svg').then(data => data.text()).then(text => {this.svgLocationMarker = new H.map.Icon(text);console.log('created svg marker')});
    },
    addBubble(evt){
          // event target is the marker itself, group is a parent event target
          // for all objects that it contains
          console.log('evt data',evt.target.getPosition());
          let bubble = new H.ui.InfoBubble(evt.target.getPosition(), {
            // read custom data
            content: evt.target.getData()
          });
          // show info bubble
          this.ui.addBubble(bubble);
          bubble.addClass('containerBlob');
          // bubble.open();
    },
    addToGroup(coordinate, html) {
      console.log("add to group", coordinate);

        let marker = new H.map.Marker(coordinate,{icon: this.svgMarker});
        marker.setData(html);


      console.log("group", this.group);
      this.markers.addObject(marker);
      console.log("added to group");
    },
    updatePosition() {
      let me = null
      this.geoLoc = navigator.geolocation.watchPosition(cord => {
        console.log(cord);
        this.curPos = {lat:cord.coords.latitude,lng:cord.coords.longitude};
        if (me) { this.map.removeObject(me) }
        let svgMarkup ='<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24"><path d="M12 7c-2.76 0-5 2.24-5 5s2.24 5 5 5 5-2.24 5-5-2.24-5-5-5zm0-5C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8z"/><path d="M0 0h24v24H0z" fill="none"/></svg>';
        let icon = new H.map.Icon(svgMarkup);
        let coords = this.curPos;
        me = new H.map.Marker(coords, { icon: this.svgLocationMarker });
        this.map.addObject(me);
        if (this.show && this.firstTime) {
          this.axios({
            url: "http://192.168.81.74:5000/get-containers",
            method: "get",
            params: {
              lat: this.curPos.lat,
              lng: this.curPos.lng,
              containers: this.$route.query.containers
            }
          })
            .then(data => {
              let containers = data.data.data;
              // console.log(containers);
              console.log('PUBLIC',this.$route.query.public);
              for (let i = 0; i < containers.length; i++) {
                if(this.$route.query.public == 'false' ||this.$route.query.public == false) {
                  this.addToGroup(
                    {
                      lat: containers[i].coordinates[0],
                      lng: containers[i].coordinates[1]
                    },
                    generateMarkerBlob(containers[i]),
                  );
                }
                else if((containers[i].public)) {
                  this.addToGroup(
                    {
                      lat: containers[i].coordinates[0],
                      lng: containers[i].coordinates[1]
                    },
                    generateMarkerBlob(containers[i]),
                  );
                }
              }
            })
            .catch(err => {
              console.log("error occured", err);
            });
          this.map.setCenter({
            lat: cord.coords.latitude,
            lng: cord.coords.longitude
          });
          this.map.setZoom(17);
          this.firstTime = false;
        }},
        err => {
          console.log(err);
          return;
        },
        {
          enableHighAccuracy: true,
          timeout: 60000,
          maximumAge: 0
        }
      );
    },
    getStart() {
      this.map.setCenter(this.curPos);
      this.map.setZoom(19);
    }
  },
  mounted() {
    this.loadSVG('/container-blank.svg');
    this.createMap();
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
  position: fixed;
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

.containerBlob {
  background-color: yellow;
}
</style>
