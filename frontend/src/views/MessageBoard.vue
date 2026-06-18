<script setup>
import { reactive, ref } from 'vue'

import api from '../services/api'

const form = reactive({
  name: '',
  email: '',
  subject: '',
  content: '',
})

const loading = ref(false)
const success = ref('')
const error = ref('')

async function submitMessage() {
  loading.value = true
  success.value = ''
  error.value = ''

  try {
    await api.post('/messages/', form)
    form.name = ''
    form.email = ''
    form.subject = ''
    form.content = ''
    success.value = '留言已提交'
  } catch {
    error.value = '留言提交失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="mx-auto max-w-2xl space-y-6">
    <div>
      <h1 class="page-title">留言板</h1>
      <p class="mt-2 text-slate-600">任何访客都可以提交留言，后台仅管理员可查看。</p>
    </div>

    <form class="page-panel space-y-4" @submit.prevent="submitMessage">
      <div>
        <label for="name" class="field-label">姓名</label>
        <input id="name" v-model="form.name" class="field-input" required autocomplete="name" />
      </div>

      <div>
        <label for="email" class="field-label">邮箱</label>
        <input id="email" v-model="form.email" class="field-input" type="email" required autocomplete="email" />
      </div>

      <div>
        <label for="subject" class="field-label">主题</label>
        <input id="subject" v-model="form.subject" class="field-input" />
      </div>

      <div>
        <label for="content" class="field-label">内容</label>
        <textarea id="content" v-model="form.content" class="field-input min-h-36" required />
      </div>

      <button class="primary-button" type="submit" :disabled="loading">
        {{ loading ? '提交中...' : '提交留言' }}
      </button>

      <p v-if="success" class="text-sm font-semibold text-green-700">{{ success }}</p>
      <p v-if="error" class="text-sm font-semibold text-red-700">{{ error }}</p>
    </form>
  </section>
</template>
