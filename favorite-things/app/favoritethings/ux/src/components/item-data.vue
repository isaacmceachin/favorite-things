<template>
  <div class="main-content">
    <b-container id="container">
      <entity-modals
        :selectedCategoryToOperate="selectedCategoryToOperate"
        :setCategoryToOperate="setCategoryToOperate"
        :setListCategoriesList="setListCategoriesList"
        :setListTypeList="setListTypeList"

        :currentViewingItemName="currentViewingItemName"
        :currentViewingItem="currentViewingItem"
      />

      <div class="list-categories">
        <div v-if="currentCategoryName.length > 0" :key="refreshShowingData">
          <h1 style="float:left;">Showing {{currentCategoryName}}</h1>
          <br/><br/>
          <div style="float:right;">
            <b-button variant="outline-primary" v-b-modal.create-item>new {{currentCategoryName}}</b-button>
            <b-button variant="outline-danger" v-b-modal.remove-category>remove category</b-button>
          </div>
          <br/><br/><br/>
        </div>

        <list-things
          :setCategoryToOperate="setCategoryToOperate"
          :selectedCategoryToOperate="selectedCategoryToOperate"
          :modalDataCurrentItem="setModalDataCurrentItem"
          :refreshCB="listRefresh"
          :defaultCategory="selectedCategoryToOperate"
          :listCategoriesList="listCategoriesList"
          :listTypeList="listTypeList"/>
      </div>
    </b-container>
  </div>
</template>

<script>
  import ListThings from './list-things.vue'
  import EntityModals from './entity-modals.vue'

  import axios from 'axios';

  axios.defaults.baseURL = process.env.API_ENDPOINT;

  axios.defaults.xsrfHeaderName = "X-CSRFToken"
  axios.defaults.xsrfCookieName = 'csrftoken'

  var csrftoken;
  let getToken = document.getElementsByName("csrfmiddlewaretoken");
  if(getToken.length){
    csrftoken = getToken[0].value;
  }else{
    csrftoken = false;
  }

  const config = {
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    }
  }

  export default {
    name: "main-content",
    data: () => ({
      selectedCategoryToOperate: null,

      listCategoriesList: [],
      categoriesListKey: 0,

      listType: "",
      listTypeList: [],
      listKey: 0,

      refreshShowingData: 0,

      currentViewingItemName: null,
      currentViewingItem: null,
    }),
    created: function() {
      this.refreshCategoryList();
    },
    computed: {

    },
    methods: {
      currentCategoryName: function(){
        let {title} = this.listCategoriesList[this.categoriesListKey] || {};
        return title || '';
      },
      refreshItemList: async function(){
        if(!!this.selectedCategoryToOperate){
          console.log(this.selectedCategoryToOperate.uuid);

          let data = this.selectedCategoryToOperate;

          if(this.currentCategoryName.length > 0){
            axios
              .get(`/favoritethings/category/${this.selectedCategoryToOperate.uuid}`, data, config)
              .then(res => {
                this.listTypeList = res.data.data || [];
              }).catch(error => {
                  this.listTypeList = [];
              });
          }else{
            this.listTypeList = [];
          }
        }
      },
      refreshCategoryList: async function(){
        axios
          .get(`/favoritethings/categories`, config)
          .then(res => {
            this.listCategoriesList = res.data.data || [];
            if(this.listCategoriesList.length){

              this.selectedCategoryToOperate = this.listCategoriesList[0];
              this.refreshItemList();
            }
          }).catch(error => {
              this.listCategoriesList = [];
          });
      },

      setListCategoriesList: async function(list, key = -1){

        if(key > -1){
          this.refreshItemList()
        }else{
          this.categoriesListKey = key;
          this.listCategoriesList = list;
          this.refreshCategoryList();
        }

        this.refreshShowingData += 1;
      },
      setListTypeList: async function(list, key = 0){
        this.listKey = key;
        this.listTypeList = list;
        this.refreshItemList();
      },

      listRefresh: async function(e){
        console.log("Test", e);

        let selectedKey = -1;
        this.listCategoriesList.forEach((item, key) => {
          if(item.uuid == e){
            this.categoriesListKey = key;
            this.selectedCategoryToOperate = this.listCategoriesList[this.categoriesListKey];
            axios
              .get(`/favoritethings/category/${this.selectedCategoryToOperate.uuid}`, {}, config)
              .then(res => {
                this.listTypeList = res.data.data || [];
              }).catch(error => {
                  this.listTypeList = [];
              });
            this.refreshShowingData += 1;
          }
        });

        if(selectedKey > -1){

        }
      },
      setModalDataCurrentItem: async function(value){
        console.log("Meta", value);
        this.currentViewingItem = value;
      },

      setCategoryToOperate: async function(categoryValue){
        this.selectedCategoryToOperate = categoryValue;
      }
    },
    components: {
      ListThings,
      EntityModals
    }
  }
</script>
