<template>
  <div class="main-content">

    <b-container style="margin-bottom:200px;">
      <b-jumbotron header="My Favorite Things" lead="the very best of things">
      </b-jumbotron>

      <!-- The modal -->
      <b-modal id="create-category" @ok="handleCreateCategoryOk">
        <b-alert dismissible variant="warning" :show="newCategoryNameError" :key="newCategoryNameErrorKey">{{newCategoryNameError}}</b-alert>

        <template slot="modal-title">
          Create category!
        </template>

        <label for="create-category-name">Enter the name of your new category...</label>
        <b-form-input
          id="create-category-name"
          :formatter="format"
          placeholder="Category name here"
          v-model="saveCategoryForm.newCategoryName"
        ></b-form-input>
        <b-form-text id="input-formatter-help">
          Category names are converted to lowercase, and stripped of special characters!
        </b-form-text>

        <template slot="modal-footer" slot-scope="{ ok, cancel }">
          <b-button size="sm" variant="danger" @click="cancel()">
            Cancel
          </b-button>
          <b-button size="sm" variant="success" @click="ok()">
            Save Category!
          </b-button>
        </template>
      </b-modal>

      <b-modal id="remove-category" @ok="doRemoveCategory">
        <template slot="modal-title">
          Remove {{listType}} category!
        </template>
        This action will remove the {{listType}} category, and all of it's cool things!
      </b-modal>

      <b-modal id="create-item" @ok="newThingOnItem">
        <template slot="modal-title">
          Create {{listType}} item!
        </template>

        <p style="margin:20px;border:1px solid black;">
          {{ this.selectedCategoryToOperate }}
        </p>

        <div>
          <b-alert dismissible variant="warning" :show="itemDescriptionLengthError" :key="itemDescriptionLengthErrorKey">Please ensure the description is longer than 10 characters...</b-alert>

          <b-form>
            <b-form-group id="input-group-2" label-for="input-2">
              <b-input
                required
                v-model="newThingItemForm.itemName"
                placeholder="Enter name">
              </b-input>

              <br/>

              <b-form-textarea
                required
                v-model="newThingItemForm.itemDescription"
                placeholder="Enter something...">
              </b-form-textarea>

              <br/>

              <b-form-select v-model="newThingItemForm.itemRanking" :options="options()">
                <template slot="first">
                  <option :value="false">-- New Rank --</option>
                </template>
              </b-form-select>

            </b-form-group>
          </b-form>

          {{newThingItemForm}}

          {{options()}}

          <pre class="m-0">{{ form }}</pre>

          <div v-for="(value, key) in currentMeta">
          </div>
        </div>
      </b-modal>

      <b-modal id="view-history">
        <template slot="modal-title">
          {{selectedItemName}} Details!
        </template>

        <div>
          <div v-for="(value, key) in currentViewingItem">
            <b>{{key.toUpperCase()}}:</b> {{value}}<br/>
          </div>
        </div>
      </b-modal>

      <b-button variant="outline-primary" v-b-modal.create-category>Add Category</b-button>
      <br/><br/>

      <div v-if="listCategoriesList.length > 0">
        <div v-if="listType.length > 0" :key="categoryDeleteKeyShift">
          <h1 style="float:left;">Showing {{listType}}</h1>
          <br/><br/>
          <div style="float:right;">
            <b-button variant="outline-primary" v-b-modal.create-item>new {{listType}}</b-button>
            <b-button variant="outline-danger" v-b-modal.remove-category>remove category</b-button>
          </div>
          <br/><br/><br/>
        </div>

        <b-card no-body>
          <b-tabs pills card vertical>

            <div :key="listCategoriesValue">
              <b-alert dismissible variant="warning" :show="showAlert">Empty list!</b-alert>
              <h1 v-if="showAlert" style="margin-left:15px;margin-top:15px;"><u>
                Add new {{listType}} items!
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
        <center><h1><b-alert dismissible variant="warning" :show="listType.length == 0">Please create new categories</b-alert></h1></center>
      </div>
    </b-container>

  </div>
</template>

<script>
  import axios from 'axios';

  axios.defaults.baseURL = process.env.API_ENDPOINT;

  axios.defaults.xsrfHeaderName = "X-CSRFToken"
  axios.defaults.xsrfCookieName = 'csrftoken'
  //axios.defaults.withCredentials = true

  var csrftoken;
  let getToken = document.getElementsByName("csrfmiddlewaretoken");
  if(getToken.length){
    csrftoken = getToken[0].value;
  }else{
    csrftoken = false;
  }

  /*console.log({
    csrftoken
  });*/

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
      listCategoriesList: [],
      categoriesListKey: 0,

      listType: "",
      listTypeList: [],
      listKey: 0,

      fields: ['first_name', 'last_name', 'age'],
      items: [
        { isActive: true, age: 40, first_name: 'Dickerson', last_name: 'Macdonald' },
        { isActive: false, age: 21, first_name: 'Larsen', last_name: 'Shaw' },
        { isActive: false, age: 89, first_name: 'Geneva', last_name: 'Wilson' },
        { isActive: true, age: 38, first_name: 'Jami', last_name: 'Carney' }
      ],

      form: {
      },

      selectedItemName: null,
      newCategoryNameError: false,
      newCategoryNameErrorKey: 0,
      saveCategoryForm: {
        newCategoryName: null
      },

      newThingItemForm: {
        itemName: '',
        itemDescription: '',
        itemRanking: false
      },

      selected: null,
      options: function () {
        let count = this.listTypeList.length;

        let data = [
        ];

        for(let iii = 1; iii <= count; iii++){
          let item = this.listTypeList[iii-1];
          //console.log({item});

          data.push({value: {
            set: iii,
            uuid: item.uuid,
            title: item.title,
          }, text: `Rank ${iii}`});
        }

        return data;
      },

      selectedCategoryToOperate: null,
      categoryDeleteKeyShift: 0,
      currentMeta: () => {

        return [];
      },
      currentViewingItem: null,
      itemDescriptionLengthError: false,
      itemDescriptionLengthErrorKey: 0
    }),
    created: function() {
      this.checkCategoryList();
      this.checkTypesList();
    },
    computed: {
      showAlert: function(){
        return this.listTypeList.length == 0 && this.listType.length > 0;
      },
      listKeyValue: function(){
        return `LIST-${this.listKey}`;
      },

      listCategoriesValue: function(){
        return `CAT-LIST-${this.categoriesListKey}`;
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
        this.checkTypesList();
      },
      checkTypesList: async function(){
        if(!!this.selectedCategoryToOperate){
          console.log(this.selectedCategoryToOperate.uuid);

          let data = this.selectedCategoryToOperate;

          if(this.listType.length > 0){
            axios
              .get(`/favoritethings/category/${this.selectedCategoryToOperate.uuid}`, data, config)
              //.get(`/favoritethings/category/${this.listType}`, config)
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
      checkCategoryList: async function(){
        axios
          .get(`/favoritethings/categories`, config)
          .then(res => {
            this.listCategoriesList = res.data.data || [];
            if(this.listCategoriesList.length){
              this.listType = this.listCategoriesList[0].title;

              let setTo = this.listCategoriesList.filter( (item) => {
                return item.title == this.listType
              } )[0];

              this.selectedCategoryToOperate = setTo;

              this.checkTypesList();
            }
          }).catch(error => {
              this.listCategoriesList = [];
          });
      },
      categoryItemClick: async function(evt, valueParam){

        evt.preventDefault();
        let value = evt.target.text.replace(/\s\([0-9]+\)/, "").trim();
        this.listType = value;

        let setTo = this.listCategoriesList.filter( (item) => {
          return item.title == this.listType
        } )[0];

        this.selectedCategoryToOperate = setTo;

        this.onNewList(evt);
        console.log({valueParam, setTo});
      },
      doRemoveCategory: async function() {
        console.log("out", this.selectedCategoryToOperate);

        const fin = () => {
          this.listCategoriesList = [];
          this.categoriesListKey =  0;

          this.listType = "";
          this.listTypeList = [];
          this.listKey = 0;
          this.selectedCategoryToOperate = null;

          this.listCategoriesList = [];
          this.checkCategoryList();
          this.checkTypesList();
          this.categoryDeleteKeyShift += 1;
        };

        await axios
          .delete(`/favoritethings/category/${this.selectedCategoryToOperate.uuid}`, config)
          .then(res => {
            console.log(res.data);

            fin();
          }).catch(error => {
            console.log(error);

            fin();
          });
      },

      newThingOnItem: async function(evt) {
        console.log("Event::newThingOnItem", this.newThingItemForm, "On", this.selectedCategoryToOperate);

        console.log("wa", this.newThingItemForm.itemRanking);

        const fin = () => {
          this.newThingItemForm = {
            itemName: '',
            itemDescription: '',
          };

          axios
            .get(`/favoritethings/category/${this.selectedCategoryToOperate.uuid}`, config)
            //.get(`/favoritethings/category/${this.listType}`, config)
            .then(res => {
              this.listType = this.selectedCategoryToOperate.title;
              this.listTypeList = res.data.data || [];

            }).catch(error => {
                this.listTypeList = [];
            });
        }

        console.log("oi item", this.newThingItemForm);

        let rank = 1;
        if(!this.newThingItemForm.itemRanking){
          let lenc = this.options().length;
          rank = lenc > rank ? lenc : rank;
        }else{
          rank = this.newThingItemForm.itemRanking.set;
        }

        if(! ( !!this.newThingItemForm.itemDescription && this.newThingItemForm.itemDescription.length >= 10 )){
          this.itemDescriptionLengthError = true;
          this.itemDescriptionLengthErrorKey += 1;
          return;
        }

        console.log("Fs", {rank});

        var bodyFormData = new FormData();
        bodyFormData.set('categoryTitle', this.newThingItemForm.itemName);
        bodyFormData.set('description', this.newThingItemForm.itemDescription);
        bodyFormData.set('ranking', rank);
        bodyFormData.set('meta_data', JSON.stringify({}));
        bodyFormData.set('category', this.selectedCategoryToOperate.uuid);

        await axios
          .post(`/favoritethings/category/${this.selectedCategoryToOperate.uuid}`, bodyFormData, config)
          .then(res => {
            console.log(res.data.data);
            this.listCategoriesList = res.data.data;
            //this.checkCategoryList();
            fin();
          }).catch(error => {
            console.log(error);
            this.checkCategoryList();
            fin();
          });
      },


      handleCreateCategoryOk: async function(evt) {
        if(!this.saveCategoryForm.newCategoryName){
          evt.preventDefault();
          this.newCategoryNameErrorKey += 1;
          this.newCategoryNameError = "Please enter a valid name...";
        }else{

          let cont = true;
          await this.listCategoriesList.forEach(async (item, index) => {
            if(item.title == this.saveCategoryForm.newCategoryName){
              evt.preventDefault();
              this.newCategoryNameErrorKey += 1;
              this.newCategoryNameError = "Please enter a new name...";
              cont = false;
            }
          });

          if(!cont){
            evt.preventDefault();
            return;
          }

          var bodyFormData = new FormData();
          bodyFormData.set('categoryTitle', this.saveCategoryForm.newCategoryName);

          const fin = () => {
            this.saveCategoryForm.newCategoryName = "";
          }

          await axios
            .post(`/favoritethings/categories/`, bodyFormData, config)
            .then(res => {
              console.log(res.data.data);
              this.listCategoriesList = res.data.data;
              this.checkCategoryList();
              fin();
            }).catch(error => {
              console.log(error);
              this.checkCategoryList();
              fin();
            });
        }
      },
      setCurrentItem: async function (value){
        this.selectedItemName = value.title;
        this.currentViewingItem = value;
      }
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
</style>
