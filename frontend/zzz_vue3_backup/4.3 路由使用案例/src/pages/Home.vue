<template>
  <div>
    <h2>首页</h2>
    <button @click="getCurrentUser" :disabled="loadingMe">查看当前用户信息</button>
    <button @click="getAllUsers" :disabled="loadingAll" style="margin-left: 16px;">查看所有用户信息</button>

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

    <!-- 所有用户信息展示 -->
    <div v-if="usersAll.length > 0" style="margin-top: 20px;">
      <h3>所有用户信息</h3>
      <table border="1" cellpadding="6">
        <thead>
          <tr>
            <th>ID</th>
            <th>邮箱</th>
            <th>用户名</th>
            <th>角色</th>
            <th>邮箱验证</th>
            <th>创建时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in usersAll" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.role }}</td>
            <td>{{ user.is_email_verified ? '已验证' : '未验证' }}</td>
            <td>{{ user.created_at }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="error" style="color:red; margin-top: 20px;">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
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

async function getAllUsers() {
  error.value = ''
  usersAll.value = []
  loadingAll.value = true
  try {
    const res = await axios.get('/users/all')
    usersAll.value = res.data
  } catch (e) {
    error.value = e.response?.data?.message || '获取所有用户信息失败'
  } finally {
    loadingAll.value = false
  }
}
</script>