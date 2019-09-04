<template>
  <div class="list-things">
    <div v-if="listCategoriesList.length > 0">
      <b-card no-body>
        <b-tabs pills card vertical>

          <div :key="listCategoriesValue">
            <b-alert dismissible variant="warning" :show="showAlert">Empty list!</b-alert>
            <h1 v-if="showAlert" style="margin-left:15px;margin-top:15px;"><u>
              Add new {{currentCategoryName}} items!
            </u></h1>

            <div v-for="(value, key) in listCategoriesList">
              <b-tab :title="value.title + ' (' + value.subthings + ')'" v-on:click="categoryItemClick($event, value)">
                <b-card-text>
                  <div v-for="(value, key) in listTypeList">
                    <b-card
                      :title="value.title"
                      tag="article"
                      style="max-width: 20rem;float:left;margin-right:15px;"
                      class="mb-2"
                    >
                      <b-card-text>
                        {{ value.description }}
                      </b-card-text>

                      <p>
                        <b>Ranking:</b> {{value.ranking}}
                          <br/>
                        <b>Created:</b> <timeago :datetime="value.created_on"></timeago>
                          <br/>
                        <b>Last Edit:</b> <timeago :datetime="value.modify_on"></timeago>
                      </p>

                      <b-button href="#" variant="primary" v-b-modal.view-history v-on:click="setCurrentItem(value)">Item Details</b-button>
                    </b-card>
                  </div>
                </b-card-text>
              </b-tab>
            </div>
          </div>
        </b-tabs>
      </b-card>
    </div>
    <div v-else>
      <center><h1><b-alert dismissible variant="warning" :show="currentCategoryName.length == 0">Please create new categories</b-alert></h1></center>
    </div>
  </div>
</template>

<script>
  import axios from '@/api-services/init.js'
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
      //'X-CSRFToken': csrftoken
    }
  }

  export default {
    name: "list-things",
    data: () => ({
      categoriesListKey: 0,
    }),
    created: function() {

    },
    computed: {
      showAlert: function(){
        //check if prop array listTypeList, and the name of it's category are valid
        return this.listTypeList.length == 0 && this.currentCategoryName.length > 0;
      },

      listCategoriesValue: function(){
        return `CAT-LIST-${this.categoriesListKey}`;
      },

      currentCategoryName: function(){
        let {title} = this.listCategoriesList[this.categoriesListKey] || {};
        return title || '';
      }
    },
    methods: {
      format(value, event) {
        let desired = value.replace(/[^\w\s]/gi, '');
        return desired.toLowerCase();
      },

      onNewList: async function (evt) {
        evt.preventDefault();
        this.listKey += 1;
        //this.checkTypesList();
      },
      categoryItemClick: async function(evt, valueParam){


        evt.preventDefault();
        let value = evt.target.text.replace(/\s\([0-9]+\)/, "").trim();
        let setTo = this.listCategoriesList.filter( (item) => {
          return item.title == value
        } )[0];


        console.log({valueParam, setTo});

        this.callRefresh(setTo.uuid)

        this.setCategoryToOperate(setTo);

        this.onNewList(evt);
      },

      setCurrentItem: async function (value){
        if(typeof this.modalDataCurrentItem == 'function'){
          this.modalDataCurrentItem(value);
        }
      },

      callRefresh: async function (value){
        if(typeof this.refreshCB == 'function'){
          this.refreshCB(value);
        }
      },
    },
    props: {
      selectedCategoryToOperate: {},
      setCategoryToOperate: {},
      listCategoriesList: {},
      listTypeList: {},
      defaultCategory: {},
      refreshCB: null,
      modalDataCurrentItem: null
    }
  }
</script>

<style scoped>
  /*
   * Some styles so that our first component
   * looks somewhat special
  */
  .list-things {

  }
</style>
