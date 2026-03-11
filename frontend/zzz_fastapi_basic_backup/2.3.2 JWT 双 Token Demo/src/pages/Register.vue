<template>
  <h2>用户组测</h2>
  <form @submit.prevent="handleRegister">
    <div>
      <label>邮箱：</label>
      <input v-model="form.email" type="email" required />
    </div>
    <div>
      <label>用户名：</label>
      <input v-model="form.username" type="text" required />
    </div>
    <div>
      <label>密码：</label>
      <input v-model="form.password" type="password" required />
    </div>
    <button type="submit" :disabled="loading">注册</button>
    <div v-if="error" style="color:red;">{{ error }}</div>
    <div v-if="success" style="color:green;">
      注册成功！用户ID：{{ result.id }}，注册时间：{{ result.created_at }}
    </div>
  </form>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from '../utils/request'


const form = reactive({
  email: '',
  username: '',
  password: ''
})

const loading = ref(false)
const error = ref('')
const success = ref(false)
const result = reactive({
  id: '',
  created_at: ''
})

async function handleRegister() {
  error.value = ''
  success.value = false
  loading.value = true
  console.log(import.meta.env.VITE_API_BASE_URL) 
  try {
    // 这里假设后端需要 password_hash，前端简单用明文密码（实际应加密）
    const response = await axios.post('/users/register', {
      username: form.username,
      password: form.password,
      email: form.email,
    })
    console.log(response)
    result.id = response.data.id
    result.created_at = response.data.created_at
    success.value = true
  } catch (e) {
    error.value = e.response?.data?.message || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>