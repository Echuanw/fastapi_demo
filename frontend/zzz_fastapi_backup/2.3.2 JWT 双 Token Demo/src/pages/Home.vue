<template>
  <h2>首页</h2>
  <div style="text-align:center; margin-top: 100px;">
    <button @click="goToMe" style="margin-right: 20px;">查看当前用户信息</button>
    <button @click="goToAll" style="margin-right: 20px;">查看所有用户信息</button>
    <button @click="logout">注销</button>
  </div>
  <div v-if="error" style="color:red;">{{ error }}</div>
  <div v-if="success" style="color:green;">
      注销成功！Message: {{ success }}
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import axios from '../utils/request'


const error = ref('')
const success = ref('')

const router = useRouter()
const userStore = useUserStore()

function goToMe() {
  router.push('/user') // 跳转到当前用户信息页
}

function goToAll() {
  router.push('/users') // 跳转到所有用户信息页
}

async function logout() {
  try {
    // 清楚本地 access token 和 refresh token
    const response = await axios.post('/users/logout')
    success.value = response.data.message
  } catch (e) {
    error.value = e.response?.data?.detail || '登录失败'
  } finally {
    userStore.clearAccessToken()
    setTimeout(  () => router.push('/login'), 1000)
  }
  
}
</script>