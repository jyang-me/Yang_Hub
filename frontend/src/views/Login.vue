<script setup>
import { reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const form = reactive({
  username: '',
  password: '',
})

async function submitLogin() {
  await authStore.login(form)
  await router.push(route.query.redirect || '/')
}
</script>

<template>
  <section class="mx-auto max-w-md space-y-6">
    <div>
      <h1 class="page-title">管理员登录</h1>
      <p class="mt-2 text-slate-600">登录后，Axios 请求会自动携带 Bearer Token。</p>
    </div>

    <form class="page-panel space-y-4" @submit.prevent="submitLogin">
      <div>
        <label for="username" class="field-label">用户名</label>
        <input id="username" v-model="form.username" class="field-input" required autocomplete="username" />
      </div>

      <div>
        <label for="password" class="field-label">密码</label>
        <input
          id="password"
          v-model="form.password"
          class="field-input"
          type="password"
          required
          autocomplete="current-password"
        />
      </div>

      <button class="primary-button w-full" type="submit" :disabled="authStore.loading">
        {{ authStore.loading ? '登录中...' : '登录' }}
      </button>

      <p v-if="authStore.isAuthenticated" class="text-sm font-semibold text-green-700">
        已登录：{{ authStore.user?.username || '管理员' }}
      </p>
      <p v-if="authStore.error" class="text-sm font-semibold text-red-700">
        {{ authStore.error }}
      </p>
    </form>
  </section>
</template>
