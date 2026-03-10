<!-- 父组件的 template 定义，中间调用了子组件 <HelloWorld /> -->
<template>
  <div>
    <h1>父组件</h1>
    <Register />
  </div>
</template>

<script setup>
import Register from './components/Register.vue'
</script>