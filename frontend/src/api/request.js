import axios from 'axios'
import { useAuthStore } from '../stores/auth'
import router from '../router'

const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api',
  timeout: 10000,
})

request.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()

    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }

    return config
  },
  (error) => Promise.reject(error),
)

request.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.clearAuth()

      if (router.currentRoute.value.path !== '/login') {
        await router.push({
          path: '/login',
          query: { redirect: router.currentRoute.value.fullPath },
        })
      }
    }

    return Promise.reject(error)
  },
)

export default request
