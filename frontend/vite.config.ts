import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import VueSetupExtend from 'vite-plugin-vue-setup-extend'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {

  // 这里的 mode 会自动是 'development' 或 'production'
  const env = loadEnv(mode, process.cwd())
  // 这样就能拿到 .env.development 或 .env.production 里的变量
  const apiBaseUrl = env.VITE_API_BASE_URL

  return {
    plugins: [
      vue(),
      vueDevTools(),
      VueSetupExtend(),       // 新增 setup 简化语法糖 插件调用
    ],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      },
    },
    server: {
      proxy: {
        '/api': {
          target: apiBaseUrl,
          changeOrigin: true,
          rewrite: path => path.replace(/^\/api/, '')
        }
      }
    }
  }
})