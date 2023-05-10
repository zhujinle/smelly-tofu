import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
// 导入全局样式
import './assets/css/global.css'

// 导入axios
import axios from 'axios'

import './plugins/charts.js'

Vue.config.productionTip = false

// axios 设置
axios.defaults.baseURL = '/api/V1/'
Vue.prototype.$http = axios

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
