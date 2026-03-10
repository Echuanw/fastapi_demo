<template>
  <div class="person123">
    <h2>姓名：{{name}}</h2>
    <h2>年龄：{{age}}</h2>
    <button @click="changeName">修改名字</button>
    <button @click="changeAge">年龄+1</button>
    <button @click="showTel">点我查看联系方式</button>
  </div>
</template>

<script setup lang="ts" name="Person234">
  import {ref} from 'vue'
  let name = ref('张三')    // RefImpl实例，value属性是响应式的。
  let age = ref(18)
  let tel = '13888888888'  // 普通的字符串，不是ref
  
  function changeName(){
    name.value = name.value === '张三'   // 操作ref对象时候需要.value
        ? '李四' 
        : '张三'
    console.log(name.value)             // name不是响应式的，name.value是响应式的
  }
  function changeAge(){
    age.value += 1                // 操作ref对象时候需要.value
    console.log(age.value)
  }
  function showTel(){             // 网页弹窗 alert
    alert(tel)
  }
</script>  