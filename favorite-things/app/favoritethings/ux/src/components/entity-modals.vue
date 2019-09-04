<template>
  <div class="entity-modals">
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

    <b-modal id="create-item" @ok="newThingOnCategory">
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

            <b-form-select v-model="newThingItemForm.itemRanking" :options="newItemRankingOptions">
              <template slot="first">
                <option :value="false">-- New Rank --</option>
              </template>
            </b-form-select>

          </b-form-group>
        </b-form>

        {{newThingItemForm}}

        {{newItemRankingOptions}}

        <div v-for="(value, key) in newThingItemForm.currentMeta">
        </div>
      </div>
    </b-modal>

    <b-modal id="view-history">
      <template slot="modal-title">
        {{currentViewingItemName}} Details!
      </template>

      <div>
        <div v-for="(value, key) in currentViewingItem">
          <b>{{key.toUpperCase()}}:</b> {{value}}<br/>
        </div>
      </div>
    </b-modal>

    <b-button variant="outline-primary" v-b-modal.create-category>Add Category</b-button>
    <br/><br/>
  </div>
</template>

<script>
  //import CategoryService from '@/api-services/category.service';
  import axios from '../api-services/init.js'

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
    name: "entity-modals",
    data: () => ({
      listCategoriesList: [],
      categoriesListKey: 0,

      listType: "",
      listTypeList: [],
      listKey: 0,

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

      refreshShowingData: 0,

      itemDescriptionLengthError: false,
      itemDescriptionLengthErrorKey: 0,
      currentMeta: () => {

        return [];
      },
    }),
    computed: {
      newItemRankingOptions: function () {
        let count = this.listTypeList.length;

        let data = [
        ];

        for(let iii = 1; iii <= count; iii++){
          let item = this.listTypeList[iii-1];

          data.push({value: {
            set: iii,
            uuid: item.uuid,
            title: item.title,
          }, text: `Rank ${iii}`});
        }

        return data;
      },
      currentCategoryName: function(){
        let {title} = this.listCategoriesList[this.categoriesListKey] || {};
        return title || '';
      },
    },
    methods: {
      format(value, event) {
        let desired = value.replace(/[^\w\s]/gi, '');
        return desired.toLowerCase();
      },

      refreshItemList: async function(){
        if(!!this.selectedCategoryToOperate){
          console.log(this.selectedCategoryToOperate.uuid);

          let data = this.selectedCategoryToOperate;

          if(this.currentCategoryName.length > 0){
            axios
              .get(`/favoritethings/category/${this.selectedCategoryToOperate.uuid}`, data, config)
              .then(res => {
                this.setListTypeList(res.data.data || []);
              }).catch(error => {
                  this.setListTypeList([]);
              });
          }else{
            this.setListTypeList([]);
          }
        }
      },
      refreshCategoryList: async function(){
        axios
          .get(`/favoritethings/categories`, config)
          .then(res => {
            this.setListCategoriesList(res.data.data || [])
            if(this.listCategoriesList.length){
              this.setCategoryToOperate(this.listCategoriesList[0]);
            }
          }).catch(error => {
              this.setListCategoriesList([])
          });
      },

      doRemoveCategory: async function() {
        const fin = () => {
          this.listTypeList = [];
          this.listKey = 0;
          this.setCategoryToOperate();
          this.categoriesListKey =  0;

          this.refreshCategoryList();
          this.refreshItemList();
          this.refreshShowingData += 1;
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

      newThingOnCategory: async function(evt) {
        console.log("Event::newThingOnCategory", this.newThingItemForm, "On", this.selectedCategoryToOperate);

        console.log("itemRanking", this.newThingItemForm.itemRanking);

        const fin = () => {
          this.newThingItemForm = {
            itemName: '',
            itemDescription: '',
          };
          this.refreshItemList();
        }

        console.log("item", this.newThingItemForm);

        let rank = 1;
        if(!this.newThingItemForm.itemRanking){
          let lenc = this.newItemRankingOptions.length;
          rank = lenc > rank ? lenc : rank;
        }else{
          rank = this.newThingItemForm.itemRanking.set;
        }

        if(! ( !!this.newThingItemForm.itemDescription && this.newThingItemForm.itemDescription.length >= 10 )){
          this.itemDescriptionLengthError = true;
          this.itemDescriptionLengthErrorKey += 1;
          return;
        }

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
            //this.setListCategoriesList(res.data.data || [])
            let key = -1;
            res.data.data.forEach((item, k) => {
              if(item.uuid == this.selectedCategoryToOperate.uuid){
                key = k;
              }
            });

            this.newThingItemForm = {
              itemName: '',
              itemDescription: '',
            };
            this.setListCategoriesList(res.data.data || [], key)

          }).catch(error => {
            console.log(error);
            this.refreshCategoryList();
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
            this.refreshCategoryList();
          }

          await axios
            .post(`/favoritethings/categories/`, bodyFormData, config)
            .then(res => {
              console.log(res.data.data);
              this.setListCategoriesList(res.data.data || [], res.data.data.length)
              fin();
            }).catch(error => {
              console.log(error);
              fin();
            });
        }
      },

      listRefresh: async function(e){
        console.log("Test", e);

        let selectedKey = -1;
        this.listCategoriesList.forEach((item, key) => {
          if(item.uuid == e){
            selectedKey = key;
          }
        });

        if(selectedKey > -1){
          this.categoriesListKey = selectedKey;
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
      },
      setModalDataCurrentItem: async function(value){
        console.log("Meta", value);
        this.currentViewingItem = value;
      }
    },
    props: {
      selectedCategoryToOperate: {},
      setCategoryToOperate: {},
      setListCategoriesList: {},
      setListTypeList: {},

      currentViewingItemName: {},
      currentViewingItem: {},
    },
    components: {

    }
  }
</script>

<style scoped>
  /*
   * Some styles so that our first component
   * looks somewhat special
  */
  .entity-modals {

  }
</style>
