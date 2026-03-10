import { createApp } from 'vue'      // createApp 创建应用，理解为环境 
import App from './App.vue'          // App组件，理解为环境上的应用
import Person from './components/Person.vue'    // 全局注册组件1

const app = createApp(App)

// 通过 app.component 方法全局注册组件
app.component('Person', Person)      // 全局注册组件2
app.mount('#app')
