<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link>
      <router-link to="/map">Map</router-link>
    </div>
    <router-view/>
  </div>
</template>

<style>
* {
  box-sizing: border-box;
  word-break: break-word;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  font-size: 15px;
  font-weight: 400;
  letter-spacing: .2px;
  line-height: 1.3;
  margin: 0;
  padding: 0;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background: #f7f7f7;
  color: rgba(49, 49, 49, 0.84);
  display: block;
  height: 100vh;
  overflow-x: hidden;
}

#app {
  display: flex;
  flex-direction: column;
  height: 100%;
}
#nav {
  padding: 30px;
  text-align: center;
  flex: 1;
}

button {
  border: none;
  background: inherit;
  cursor: pointer;
}

button:focus {
  outline: none;
}

#nav a {
  font-weight: 900;
  color: #2c3e50;
  text-decoration: none;
  text-transform: uppercase;
}

#nav a.router-link-exact-active {
  color: #565a5a;
}

#nav a:hover {
  color: black;
}

</style>
