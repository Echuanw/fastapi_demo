<template>
  <h2>用户登录</h2>
  <form @submit.prevent="handleLogin">
    <div>
      <label>用户名：</label>
      <input v-model="form.username" type="text" required />
    </div>
    <div>
      <label>密码：</label>
      <input v-model="form.password" type="password" required />
    </div>
    <button type="submit" :disabled="loading">登录</button>
    <div v-if="error" style="color:red;">{{ error }}</div>
    <div v-if="accessToken" style="color:green;">
      登录成功！access_token: {{ accessToken }}
    </div>
  </form>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from '../utils/request'
import { useUserStore } from '../stores/user'
import { useRouter } from 'vue-router'


const router = useRouter()
const userStore = useUserStore()
const form = reactive({
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')
const accessToken = ref('')

async function handleLogin() {
  error.value = ''
  accessToken.value = ''
  loading.value = true
  try {
    const response = await axios.post('/users/login', {
      username: form.username,
      password: form.password
    })
    // 将 accessToken.value 提交到全局状态管理（如 pinia），以便其他组件使用
    userStore.setAccessToken(response.data.token_type, response.data.access_token)

    // 跳转到主页
    setTimeout(()=>{
        router.push('/home') 
      },1500)

  } catch (e) {
    error.value = e.response?.data?.detail || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>