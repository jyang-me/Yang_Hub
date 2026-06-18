import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

import request from '../api/request'

const TOKEN_KEY = 'auth_token'
const USER_KEY = 'auth_user'

function readStoredUser() {
  const rawUser = localStorage.getItem(USER_KEY)

  if (!rawUser) {
    return null
  }

  try {
    return JSON.parse(rawUser)
  } catch {
    localStorage.removeItem(USER_KEY)
    return null
  }
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem(TOKEN_KEY) || '')
  const user = ref(readStoredUser())
  const loading = ref(false)
  const error = ref('')

  const isAuthenticated = computed(() => Boolean(token.value))

  function setAuth(nextToken, nextUser = null) {
    token.value = nextToken || ''
    user.value = nextUser

    if (token.value) {
      localStorage.setItem(TOKEN_KEY, token.value)
    } else {
      localStorage.removeItem(TOKEN_KEY)
    }

    if (user.value) {
      localStorage.setItem(USER_KEY, JSON.stringify(user.value))
    } else {
      localStorage.removeItem(USER_KEY)
    }
  }

  function clearAuth() {
    setAuth('', null)
  }

  async function fetchCurrentUser() {
    const response = await request.get('/auth/me/')
    user.value = response.data
    localStorage.setItem(USER_KEY, JSON.stringify(response.data))
    return response.data
  }

  async function login(credentials) {
    loading.value = true
    error.value = ''

    try {
      const response = await request.post('/auth/token/', credentials)
      setAuth(response.data.token, null)
      await fetchCurrentUser()
      return response.data.token
    } catch (err) {
      clearAuth()
      error.value = '用户名或密码不正确'
      throw err
    } finally {
      loading.value = false
    }
  }

  function logout() {
    clearAuth()
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    setAuth,
    clearAuth,
    fetchCurrentUser,
    login,
    logout,
  }
})
