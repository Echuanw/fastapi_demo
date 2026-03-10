import { createApp } from 'vue'      // createApp 创建应用，理解为环境 
import App from './App.vue'          // App组件，理解为环境上的应用
import HelloWorld from './HelloWorld.vue'    // 全局注册组件1，在main.ts中导入

const app = createApp(App)

// 通过 app.component 方法全局注册组件
app.component('HelloWorld', HelloWorld)      // 全局注册组件2，在main.ts中通过 app.component 方法注册组件
app.mount('#app')
