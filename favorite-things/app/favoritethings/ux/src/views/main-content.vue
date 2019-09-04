<template>
  <div class="main-content">
    <b-container id="container">
      <favorite-header/>
      <item-data/>
    </b-container>
  </div>
</template>

<script>
  import FavoriteHeader from '../components/favorite-header.vue'
  import ItemData from '../components/item-data.vue'

  export default {
    name: "main-content",
    data: () => ({}),
    created: function(){
    },
    computed: {},
    methods: {},
    components: {
      FavoriteHeader,
      ItemData
    }
  }
</script>

<style scoped>
  /*
   * Some styles so that our first component
   * looks somewhat special
  */
  .main-content {

  }
  #container{
    margin-bottom:200px;
  }
</style>
