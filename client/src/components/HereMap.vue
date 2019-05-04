<template>
  <div>
    <div class="here-map">
      <div ref="map" v-bind:style="{ width: width, height: height }"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "HereMap",
  data() {
    return {
      map: {},
      platform: {},
      location: {},
      containers: {}
    };
  },
  props: {
    appId: String,
    appCode: String,
    width: String,
    height: String
  },
  created() {
    this.platform = new H.service.Platform({
      app_id: this.appId,
      app_code: this.appCode
    });
  },
  mounted() {
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
    var ui = H.ui.UI.createDefault(this.map, layers);
    this.location = null;

    navigator.geolocation.watchPosition(cord => {
      if (!this.location) {
        this.location = {lat:cord.coords.latitude,lng:cord.coords.longitude};
        this.axios({
          url:'http://localhost:5000/get-containers',
          method: 'get',
          params: {
            lat: this.location.lat,
            lng: this.location.lng,
            containers:[1].join(','),
          }
        }).then((data)=>{
          console.log(data);
          // for(location in data.data){
          //   console.log('adding marker')
          //   let marker = new H.map.Marker({lat:location.coordinates[0], lng:location.coordinates[0]});
          //   this.map.addObject(marker);
          // }
          }).catch((err)=>{console.log('error occured',err)})
      }

      this.map.setCenter({
        lat: cord.coords.latitude,
        lng: cord.coords.longitude
      });
      this.map.setZoom(17);
    });
  }
};
</script>