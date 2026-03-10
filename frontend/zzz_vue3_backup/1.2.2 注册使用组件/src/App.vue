<!-- 父组件的 template 定义，中间调用了子组件 <HelloWorld /> -->
<template>
  <div>
    <h1>父组件</h1>
    <HelloWorld />
  </div>
</template>

<script setup>
// 局部注册组件，父组件的 scritp 中 注册了 HelloWorld 组件，所以只能在当前父组件内可用
// 如果是全局注册的，旧不需要再这里导入了。直接再 template 中调用即可
// import HelloWorld from './HelloWorld.vue'
</script>