import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import UserList from '../pages/UserList.vue'
import Register from '../pages/Register.vue'
import Login from '../pages/Login.vue'
import UserInfo from '../pages/UserInfo.vue'
import { useUserStore } from '../stores/user'


// 指定地址和路由组件的对应关系
// 给路由规则命名可以简化路由跳转及传参
const routes = [ 
  { name: 'zhuye', path: '/home', component: Home },
  { name: 'users', path: '/users', component: UserList },
  { name: 'register', path: '/register', component: Register },
  { name: 'login', path: '/login', component: Login },
  { name: 'user', path: '/user', component: UserInfo },
  { path:'/', redirect:'/home' }    // 重定向，访问 / 会自动转到 /home
]

const router = createRouter({
  history: createWebHistory(),  // 路由器的工作模式为 history
  routes
})

// 路由守卫, 如果
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.path === '/login' && userStore.accessToken != '') {
    alert("已登录，跳转到主页")
    setTimeout(()=>{
        next('/home')
      },1500)
  } else {
    next() // 其他情况正常访问
  }
})

export default router