import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../components/Log-in.vue'
import Home from '../components/home.vue'
import Welcome from '../components/Welcome.vue'
import userlist from '../components/user/userlist.vue'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    { path: '/', redirect: '/Login' },
    { path: '/login', component: Login },
    {
      path: '/home',
      component: Home,
      redirect: '/Welcome',
      children: [
        { path: '/Welcome', component: Welcome },
        { path: '/userlist', component: userlist }
      ]
    }
  ]
})

// 路由导航守卫
router.beforeEach((to, from, next) => {
  // to将要访问的资源
  // from 从哪里跳转来
  // next 是函数，表示将要放行。 next('/login') 强制跳转
  if (to.path === '/login') return next()
  // Get Token
  const SceretKey = window.sessionStorage.getItem('SecretKey')
  if (!SceretKey) {
    return next('/login')
  }
  next()
})
export default router
