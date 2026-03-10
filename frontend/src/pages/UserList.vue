<template>
  <div>
    <div v-if="error" style="color:red;">{{ error }}</div>
    <table v-if="users.length > 0" border="1" cellpadding="6" style="margin-top:16px;">
      <thead>
        <tr>
          <th>ID</th>
          <th>邮箱</th>
          <th>用户名</th>
          <th>角色</th>
          <th>邮箱验证</th>
          <th>创建时间</th>
          <th>更新时间</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.role }}</td>
          <td>{{ user.is_email_verified ? '已验证' : '未验证' }}</td>
          <td>{{ user.created_at }}</td>
          <td>{{ user.updated_at }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else-if="!loading">暂无用户数据</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from '../utils/request'

const users = ref([])
const loading = ref(false)
const error = ref('')

async function fetchUsers() {
  error.value = ''
  loading.value = true
  try {
    const response = await axios.get('/users/all')
    users.value = response.data
  } catch (e) {
    error.value = e.response?.data?.message || '获取用户失败'
  } finally {
    loading.value = false
  }
}
await fetchUsers()
</script>