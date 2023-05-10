import Vue from 'vue'
import App from './App.vue'
import router from './router'
import './plugins/element.js'
// 导入全局样式
import './assets/css/global.css'
// 导入axios
import axios from 'axios'

Vue.config.productionTip = false

// axios 设置
axios.defaults.baseURL = '/api/V1/'
Vue.prototype.$http = axios
axios.interceptors.request.use(config => {
  console.log(config)
  config.headers.Authorization = window.sessionStorage.getItem('SecretKey')
  return config
})

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
