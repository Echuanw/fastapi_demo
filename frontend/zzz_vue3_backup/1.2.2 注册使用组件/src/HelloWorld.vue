<!-- 首先，定义了子组件 HelloWorld -->
<template>
  <div>
    <!-- {{ }} 调用 ref 对象 -->
    <h2>{{ message }}</h2>
    <!-- @click 点击事件调用 changeMessage 方法 -->
    <button @click="changeMessage">点击切换消息</button>
  </div>
</template>

<!-- script 中的返回值，都可以在 template 中调用 -->
<script setup>
import { ref } from 'vue'

const message = ref('你好，Vue 3 组件！')

function changeMessage() {
  message.value = message.value === '你好，Vue 3 组件！'  // 三元运算符的全等判断
    ? '你点击了按钮！'                                    // True Statement
    : '你好，Vue 3 组件！'                               // False Statement
}
</script>

<style scoped>
h2 {
  color: #42b983;
}
</style>