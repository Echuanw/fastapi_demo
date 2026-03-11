<!-- 父组件的 template 定义，中间调用了子组件 <HelloWorld /> -->
<template>
  <div>
    <nav>
        <ul>
          <li><router-link to="/">首页</router-link></li>
          <li><router-link to="/users">用户列表</router-link></li>
          <li><router-link to="/register">注册</router-link></li>
          <li><router-link to="/login">登录</router-link></li>
          <li><router-link to="/user">用户详情</router-link></li>
        </ul>
    </nav>
    <br/>
    <router-view />
  </div>
</template>

<script setup>
</script>