import { createApp } from 'vue'      // createApp 创建应用，理解为环境 
import App from './App.vue'          // App组件，理解为环境上的应用

createApp(App).mount('#app')
// 前端的根地址上的指定div上部署App应用
	// 环境 ：前端的根地址
	// 部署的应用 ： App
	// 部署的位置 : 前端根地址上名为 #app 的dev