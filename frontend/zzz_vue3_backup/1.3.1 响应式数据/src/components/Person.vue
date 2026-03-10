<template>
  <div class="person">
    <h2>姓名：{{person.name}}</h2>
    <h2>年龄：{{person.age}}</h2>
    <button @click="changeName">修改名字</button>
    <button @click="changeAge">修改年龄</button>
  </div>
</template>

<script lang="ts" setup name="Person">
  import {reactive,toRefs,toRef} from 'vue'

  // 数据
  let person = reactive({
    name:'张三',
    age:18
  })

  // let {name,age} = person       // 这种是深拷贝，相当于创建了个新的属性，且不是响应式的。后续直接修改name age不会影响响应式对象person中的 name age
  let {name,age} = toRefs(person)  // toRefs 接收响应式对象，解析并指向对象中所有的响应式属性。name age 指向 person 响应式对象中的 name age 也是响应式对象
  let nl = toRef(person,'age')     // toRef 只解析一个响应式对象的属性
  
  console.log(nl.value)

  // 方法
  function changeName(){
    name.value += '~'
    console.log(name.value,person.name)
  }
  function changeAge(){
    age.value += 1
  }

</script>