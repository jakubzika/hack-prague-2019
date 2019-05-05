<template>
    <div id="app">
        <HereMap
            appId="Muta3a1pg63jJhHuVmZP"
            appCode="eNMUIwEeBhtuXRuzmmgJhw"
            lat="37.7397"
            lng="-121.4252"
            width="100%"
            height="100%" />
    </div>
</template>

<script>
    import HereMap from "../components/HereMap.vue"

    export default {
        name: 'app',
        components: {
            HereMap
        }
    }
</script>