<template>
  <div>
    <!-- 当前用户信息展示 -->
    <div v-if="userMe" style="margin-top: 20px;">
      <h3>当前用户信息</h3>
      <ul>
        <li>ID: {{ userMe.id }}</li>
        <li>邮箱: {{ userMe.email }}</li>
        <li>用户名: {{ userMe.username }}</li>
        <li>角色: {{ userMe.role }}</li>
        <li>邮箱验证: {{ userMe.is_email_verified ? '已验证' : '未验证' }}</li>
        <li>创建时间: {{ userMe.created_at }}</li>
      </ul>
    </div>

    <div v-if="error" style="color:red; margin-top: 20px;">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from '../utils/request'

const userMe = ref(null)
const usersAll = ref([])
const loadingMe = ref(false)
const loadingAll = ref(false)
const error = ref('')

async function getCurrentUser() {
  error.value = ''
  userMe.value = null
  loadingMe.value = true
  try {
    const res = await axios.get('/users/me')
    userMe.value = res.data
  } catch (e) {
    error.value = e.response?.data?.message || '获取当前用户信息失败'
  } finally {
    loadingMe.value = false
  }
}

onMounted(() => {
  getCurrentUser()
})
</script>