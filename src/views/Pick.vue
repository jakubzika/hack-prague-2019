<template>
  <div class="container">
    <div class="map">
      <HereMap
        appId="Muta3a1pg63jJhHuVmZP"
        appCode="eNMUIwEeBhtuXRuzmmgJhw"
        width="100%"
        height="100%"
        :show=showMap
      />
    </div>
    <div v-if="!showMap" class="pick" :class="removeOverlay">
      <button class="arrow" @click="nextLeft()">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>
      </button>
      <div class="img-container">
        <img v-bind:src="require(`@/assets/trash-svg/${cur.src}.svg`)" v-bind:alt="cur.name">
      </div>
      <div class="bottom-nav">
        <div class="input-public">
          <button :class="activePublic" @click="toggleButton">Public</button>
          <button :class="activePrivate" @click="toggleButton">Private</button>
        </div>
        <input type="checkbox" v-model="checked">
        <button class="send" @click="send">Find</button>
      </div>
      <button class="arrow" @click="nextRight()">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/><path d="M0 0h24v24H0z" fill="none"/></svg>
      </button>
    </div>
  </div>
</template>

<script>
import { constants } from 'fs';
import router from '../router'
import HereMap from "../components/HereMap.vue"

export default {
  components: { HereMap },
  data: () => {
    return {
      public: true,
      showMap: false,
      cord: null,
      cur: null,
      containers: [
        {
          src: "glass",
          name: "Color glass",
          check: false,
          enum: "1"
        },
        {
          src: "electronic-devices",
          name: " Electric devices",
          check: false,
          enum: "2"
        },
        {
          src: "metals",
          name: "Metals",
          check: false,
          enum: "3"
        },
        {
          src: "beverage-cartons",
          name: "Beverage cartons",
          check: false,
          enum: "4"
        },
        {
          src: "paper",
          name: "Paper",
          check: false,
          enum: "5"
        },
        {
          src: "plastic",
          name: "Plastic",
          check: false,
          enum: "6"
        },
        {
          src: "glass",
          name: "Clear glass",
          check: false,
          enum: "7"
        },
        {
          src: "textile",
          name: "Textile",
          check: false,
          enum: "8"
        },
      ]
    }
  },
  beforeMount() {
    return this.cur = this.containers[0]
  },
  mounted() {
    if (Object.keys(this.$route.query).length !== 0) {
      this.showMap = true
    }
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(pos => {
        return this.cord = pos.coords
      }, err => {
        console.log(err)
        return
      }, {
        enableHighAccuracy : true,
        maxAge: 1000 * 2
      });
    } else {
      alert("Your phone does not support the Geolocation API");
    }
  },
  computed: {
    checked: {
      get() { return this.cur.check },
      set() { return this.cur.check = !this.cur.check }
    },
    removeOverlay: function() {
      return this.showMap ? 'invisible' : 'visible'
    },
    activePublic: function() {
      return this.public ? 'active' : ''
    },
    activePrivate: function() {
      return this.public ? 'inactive' : 'active'
    }

  },
  watch: {
    '$route.query': function(query) {
      if (query) {
        this.showMap = !this.showMap
      }
    }
  },
  methods: {
    toggleButton() {
      this.public = !this.public
    },
    send() {
      let res = []
      this.containers.map(e => {
        if (e.check) { res.push(e.enum) }
      })
      if (res.length != '0') { 
        router.push({
          path: '/',
          query: {
            containers: res.join(','),
            public: this.public,
            lat: this.cord.latitude,
            lng: this.cord.longitude
          }
        })
      }
    },
    nextLeft() {
      let num = Number(this.cur.enum) - 1
      if (num === 0) {
        return this.cur = this.containers[7]
      } else {
        return this.cur = this.containers[num - 1]
      }
    },
    nextRight() {
      let num = Number(this.cur.enum) - 1
      if (num === 7) {
        return this.cur = this.containers[0]
      } else {
        return this.cur = this.containers[num + 1]
      }
    }
  },
}
</script>

<style scoped>
img {
  width: 40%;
  min-width: 200px;
  height: 100%;
  object-fit: contain;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  z-index: -1;
  padding-bottom: 80px;
}

.container {
  display: flex;
  height: calc(100% - 79px);
  position: relative;
}

.pick {
  display: flex;
  width: 100%;
  height: 100%;
  padding-bottom: 50px;
  position: absolute;
}

.map {
  display: flex;
  flex: 1;
  position: relative;
}

.img-container {
  width: 100%;
}

.arrow:first-child {
  padding-left: 20px;
}

.arrow:nth-child(2) {
  padding-right: 20px;
}
.send {
  background: white;
  padding: 10px 25px;
  font-weight: 900;
  text-transform: uppercase;
  font-size: 1.3em;
  align-self: flex-start;
  border: 5px solid rgb(37, 37, 37);
  color: rgb(37, 37, 37);
  margin: auto;
}

.send:hover {
  background: rgb(214, 212, 212);
  border-color: black;
  color: black;
}

button svg {
  width: 80px;
  height: 80px;
  fill: rgb(153, 153, 153);
}

button svg:hover {
  fill: rgb(63, 63, 63);
}

.bottom-nav {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  bottom: 15%;
  z-index: 1;
  display: flex;
  white-space: nowrap;
}

input {
  position: relative;
  cursor: pointer;
  width: 40px;
  height: 40px;
  margin: auto 15px;
}

input[type=checkbox]:before {
  content: "";
  display: block;
  position: absolute;
  width: 40px;
  height: 40px;
  bottom: -3px;
  left: -3px;
  border: 4px solid #2c2a2a;
  background-color: white;
}

input[type=checkbox]:checked:after {
  content: "";
  display: block;
  width: 14px;
  height: 22px;
  border: solid rgb(25, 168, 101);
  border-width: 0 7px 7px 0;
  -webkit-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  transform: rotate(45deg);
  position: absolute;
  top: 0;
  left: 9px;
}
.input-public {
  display: flex;
  align-items: flex-start;
}

.input-public button{
  margin: auto;
  background: white;
  border: 4px solid rgb(37, 37, 37);
  padding: 5px 10px;
  font-weight: 900;
  text-transform: uppercase;
}

.input-public button:first-child {
  border-right: none;
}

.visible {
  z-index: 3;
  background: #f7f7f7;
}

.invisible {
  opacity: 0;
  z-index: -1
}

.active {
  background: black!important;
  color: white;
}
</style>
