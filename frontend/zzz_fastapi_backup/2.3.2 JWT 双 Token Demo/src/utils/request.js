import axios from 'axios';
import { useUserStore } from '../stores/user'


const instance = axios.create({
  baseURL: '/api',
  // baseURL: import.meta.env.VITE_API_BASE_URL, // Vue 3 Vite 项目用 import.meta.env
  // baseURL: process.env.VUE_APP_API_BASE_URL // Vue CLI 项目用 process.env
  // timeout: 1000,
  withCredentials: true, // Enable sending cookies with requests

})

// 请求拦截器
instance.interceptors.request.use(config => {
  const userStore = useUserStore()
  if (userStore.accessToken != '') {
    config.headers.Authorization = `${userStore.tokenType} ${userStore.accessToken}`
  }
  return config
})

instance.interceptors.response.use(
  response => response,
  async error => {
    const userStore = useUserStore();
    const originalRequest = error.config;

    if ((error.response.status === 401 || error.response.status === 422) && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        // 发送请求到 /refresh 端点，后端会自动从 cookie 中获取 refresh_token
        const response = await instance.post('/users/refresh');

        // 更新 access_token
        userStore.setAccessToken(response.data.token_type, response.data.access_token)

        // 重新发送原始请求
        originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;
        return axios(originalRequest);
      } catch (refreshError) {
        // 如果 refresh_token 也失效，处理用户登出
        userStore.logout();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default instance

// Vite 会根据你启动项目时的命令，自动加载对应的 .env.xxx 文件。
// 运行 npm run dev 或 vite 时，自动读取 .env 和 .env.development
// 运行 npm run build 时，自动读取 .env 和 .env.production