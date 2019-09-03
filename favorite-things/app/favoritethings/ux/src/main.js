import Vue from 'vue';

import VueTimeago from 'vue-timeago'
import BootstrapVue from 'bootstrap-vue'

require('bootstrap/dist/css/bootstrap.css');
require('bootstrap-vue/dist/bootstrap-vue.css');

Vue.use(BootstrapVue)

Vue.use(VueTimeago, {
  name: 'Timeago', // Component name, `Timeago` by default
  locale: 'en', // Default locale
  // We use `date-fns` under the hood
  // So you can use all locales from it
  /*locales: {
    'zh-CN': require('date-fns/locale/zh_cn'),
    ja: require('date-fns/locale/ja')
  }*/
})

import MainContent from './views/main-content';

let MainComponent = Vue.extend(MainContent);

new MainComponent().$mount("#app");
