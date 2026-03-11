import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'  // 在main中导入

const app = createApp(App)
app.use(router)             // 在main中调用 router
app.use(createPinia())      // 调用 pinia 插件

app.mount('#app')