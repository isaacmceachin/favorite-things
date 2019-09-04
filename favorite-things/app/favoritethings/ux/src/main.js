import Vue from 'vue';
import VueRouter from 'vue-router';

import VueTimeago from 'vue-timeago'
import BootstrapVue from 'bootstrap-vue'

//Include bootstrap css
require('bootstrap/dist/css/bootstrap.css');
require('bootstrap-vue/dist/bootstrap-vue.css');

import App from './App';

//import MainContent from './views/main-content.vue';

import routes from './routes';

//Attach required interface dependencies
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
Vue.use(VueRouter);

// Configure router
const router = new VueRouter({
    routes,
    mode: 'history'
});

//let MainComponent = Vue.extend(MainContent);

//new MainComponent().$mount("#app");

//Attach main content to the app element
new Vue({
    el: '#app',
    render: h => h(App),
    router
});
