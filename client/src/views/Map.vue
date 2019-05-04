<template>
</template>

<script>

export default {
  mounted() {
    console.log(this.$route.query)
    this.axios.get('http://localhost:5000/get-containers')
    .then((response) => {
      console.log(response.data)
    })
    .catch(err => {
      console.log(err)
    })
  }
}
</script>
