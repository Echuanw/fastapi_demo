<!-- 父组件的 template 定义，中间调用了子组件 <HelloWorld /> -->
<template>
  <div>
    <h1>父组件</h1>
    <!-- Person 全局注册 -->
    <Person />
    <line/>
    <Person2 />
  </div>
</template>

<script setup>
// Person2 局部注册
import Person2 from './components/Person2.vue';

</script>