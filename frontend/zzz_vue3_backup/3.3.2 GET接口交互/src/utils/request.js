import axios from 'axios'

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL // Vue 3 Vite 项目用 import.meta.env
  // baseURL: process.env.VUE_APP_API_BASE_URL // Vue CLI 项目用 process.env
})

export default instance

// Vite 会根据你启动项目时的命令，自动加载对应的 .env.xxx 文件。
// 运行 npm run dev 或 vite 时，自动读取 .env 和 .env.development
// 运行 npm run build 时，自动读取 .env 和 .env.production