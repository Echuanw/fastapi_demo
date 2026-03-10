<template>
  <div style="text-align:center; margin-top: 100px;">
    <button @click="goToMe" style="margin-right: 20px;">查看当前用户信息</button>
    <button @click="goToAll">查看所有用户信息</button>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()

function goToMe() {
  router.push('/user') // 跳转到当前用户信息页
}

function goToAll() {
  router.push('/users') // 跳转到所有用户信息页
}
</script>