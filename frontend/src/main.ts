import App from './App.vue'
import { createApp, ref, reactive } from 'vue'

const app = {
  setup() {
    // 页面状态
    const page = ref<'register' | 'login' | 'home' | 'me' | 'logout'>('register')
    // 全局 access_token
    const accessToken = ref<string | null>(null)
    // 注册表单
    const regForm = reactive({ email: '', username: '', password: '' })
    const regMsg = ref('')
    // 登录表单
    const loginForm = reactive({ username: '', password: '' })
    const loginMsg = ref('')
    // 个人信息
    const meInfo = ref<any>(null)

    // 注册
    const register = async () => {
      regMsg.value = ''
      try {
        const res = await fetch('/users/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(regForm)
        })
        if (res.ok) {
          regMsg.value = '注册成功，请登录'
          setTimeout(() => { page.value = 'login' }, 1000)
        } else {
          const data = await res.json()
          regMsg.value = data.detail || '注册失败'
        }
      } catch {
        regMsg.value = '网络错误'
      }
    }

    // 登录
    const login = async () => {
      loginMsg.value = ''
      try {
        const res = await fetch('/users/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(loginForm)
        })
        const data = await res.json()
        if (res.ok) {
          accessToken.value = data.access_token
          page.value = 'home'
        } else {
          loginMsg.value = data.detail || '登录失败'
        }
      } catch {
        loginMsg.value = '网络错误'
      }
    }

    // 查看个人信息
    const getMe = async () => {
      if (!accessToken.value) {
        page.value = 'login'
        return
      }
      try {
        let res = await fetch('/users/me', {
          headers: { 'Authorization': `Bearer ${accessToken.value}` }
        })
        if (res.ok) {
          meInfo.value = await res.json()
          page.value = 'me'
        } else if (res.status === 401) {
          // access_token 过期，尝试刷新
          const refreshRes = await fetch('/users/refresh', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh_token: '' }) // httpOnly Cookie 自动带上
          })
          if (refreshRes.ok) {
            const refreshData = await refreshRes.json()
            accessToken.value = refreshData.access_token
            // 重试
            res = await fetch('/users/me', {
              headers: { 'Authorization': `Bearer ${accessToken.value}` }
            })
            if (res.ok) {
              meInfo.value = await res.json()
              page.value = 'me'
              return
            }
          }
          accessToken.value = null
          page.value = 'login'
        } else {
          alert('获取个人信息失败')
        }
      } catch {
        alert('网络错误')
      }
    }

    // 注销
    const logout = async () => {
      try {
        await fetch('/users/revoke_refresh', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh_token: '' }) // httpOnly Cookie 自动带上
        })
      } catch {}
      accessToken.value = null
      page.value = 'logout'
    }

    return {
      page, regForm, regMsg, register,
      loginForm, loginMsg, login,
      getMe, meInfo,
      logout,
      accessToken
    }
  },
  template: `
    <div style="max-width:400px;margin:auto;">
      <!-- 注册页面 -->
      <div v-if="page==='register'">
        <h2>注册</h2>
        <form @submit.prevent="register">
          <input v-model="regForm.email" type="email" placeholder="邮箱" required />
          <input v-model="regForm.username" type="text" placeholder="用户名" required minlength="3" maxlength="50" />
          <input v-model="regForm.password" type="password" placeholder="密码" required minlength="6" maxlength="128" />
          <button type="submit">注册</button>
        </form>
        <div style="color:green">{{regMsg}}</div>
        <div>已有账号？<a href="#" @click.prevent="page='login'">去登录</a></div>
      </div>
      <!-- 登录页面 -->
      <div v-if="page==='login'">
        <h2>登录</h2>
        <form @submit.prevent="login">
          <input v-model="loginForm.username" type="text" placeholder="用户名" required />
          <input v-model="loginForm.password" type="password" placeholder="密码" required />
          <button type="submit">登录</button>
        </form>
        <div style="color:green">{{loginMsg}}</div>
        <div>没有账号？<a href="#" @click.prevent="page='register'">去注册</a></div>
      </div>
      <!-- 主页 -->
      <div v-if="page==='home'">
        <h2>主页</h2>
        <button @click="getMe">查看个人信息</button>
        <button @click="logout">注销</button>
      </div>
      <!-- 个人信息页面 -->
      <div v-if="page==='me'">
        <h2>个人信息</h2>
        <pre>{{JSON.stringify(meInfo, null, 2)}}</pre>
        <button @click="page='home'">返回主页</button>
      </div>
      <!-- 注销成功页面 -->
      <div v-if="page==='logout'">
        <h2>注销成功</h2>
        <div>您已安全退出。</div>
        <button @click="page='login'">重新登录</button>
      </div>
    </div>
  `
}

createApp(App).mount('#app') 