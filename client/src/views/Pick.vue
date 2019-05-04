<template>
  <div class="container">
    <button class="arrow" @click="nextLeft()">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/><path d="M0 0h24v24H0z" fill="none"/></svg>
    </button>
    <div class="img-container">
      <img v-bind:src="require(`@/assets/trash/${cur.src}.png`)" v-bind:alt="cur.name">
    </div>
    <div class="bottom-nav">
      <input type="checkbox" v-model="checked">
      <button class="send" @click="send">Send</button>
    </div>
    <button class="arrow" @click="nextRight()">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/><path d="M0 0h24v24H0z" fill="none"/></svg>
    </button>
  </div>
</template>

<script>
import { constants } from 'fs';
import router from '../router'

export default {
  data: () => {
    return {
      cord: null,
      cur: null,
      containers: [
        {
          src: "green",
          name: "Color glass",
          check: false,
          enum: "1"
        },
        {
          src: "white",
          name: " Electric devices",
          check: false,
          enum: "2"
        },
        {
          src: "grey",
          name: "Metals",
          check: false,
          enum: "3"
        },
        {
          src: "white",
          name: "Beverage cartons",
          check: false,
          enum: "4"
        },
        {
          src: "blue",
          name: "Paper",
          check: false,
          enum: "5"
        },
        {
          src: "yellow",
          name: "Plastic",
          check: false,
          enum: "6"
        },
        {
          src: "green",
          name: "Clear glass",
          check: false,
          enum: "7"
        },
        {
          src: "white",
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
    this.$watchLocation()
    .then(coordinates => {
      return this.cord = coordinates
    })
    .catch(err => {
      if (err === 'no position access') {
        alert('To use your service, allow location access')
      }
    })
  },
  computed: {
    checked: {
      get() { return this.cur.check },
      set() { return this.cur.check = !this.cur.check }
    }
  },
  methods: {
    send() {
      let res = []
      this.containers.map(e => {
        if (e.check) { res.push(e.enum) }
      })
      if (res.length != '0') { 
        this.$route.push({
          path: '/map',
          query: {
            containers: res,
            lat: this.cord.lat,
            lng: this.cord.lng
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
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.container {
  display: flex;
  flex: 1;
  height: calc(100% - 79px);
  position: relative;
  padding-bottom: 50px;
}

.img-container {
  width: 100%;
}

.arrow {
  padding: 0 20px;
}

.send {
  background: rgb(15, 172, 112);
  padding: 10px 25px;
  border-radius: 50px;
  font-weight: bold;
  font-size: 1.3em;
  align-self: flex-start;
  margin: auto;
  color: white;
  margin-left: 50px;
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
  bottom: 20%;
  z-index: 1;
  display: flex;
}

input {
  position: relative;
  margin: auto;
  cursor: pointer;
  width: 30px;
  height: 30px;
}

input[type=checkbox]:before {
  content: "";
  display: block;
  position: absolute;
  width: 30px;
  height: 30px;
  bottom: 0;
  left: 0;
  border: 3px solid #6d6b6b;
  border-radius: 3px;
  background-color: white;
}

input[type=checkbox]:checked:after {
  content: "";
  display: block;
  width: 10px;
  height: 17px;
  border: solid rgb(85, 85, 85);
  border-width: 0 5px 5px 0;
  -webkit-transform: rotate(45deg);
  -ms-transform: rotate(45deg);
  transform: rotate(45deg);
  position: absolute;
  top: 0;
  left: 9px;
}

</style>
