<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import request from '../api/request'

const posts = ref([])
const loading = ref(false)
const error = ref('')

const publishedPosts = computed(() =>
  posts.value.filter((post) => post.status === 'published' || !post.status),
)

function getPostsPayload(payload) {
  return Array.isArray(payload) ? payload : payload.results || []
}

function formatDate(value) {
  if (!value) {
    return '未发布'
  }

  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(value))
}

async function fetchPosts() {
  loading.value = true
  error.value = ''

  try {
    const response = await request.get('/posts/')
    posts.value = getPostsPayload(response.data)
  } catch (err) {
    error.value = '文章列表加载失败，请稍后重试。'
    console.error('Failed to fetch posts:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchPosts)
</script>

<template>
  <section class="space-y-8">
    <header class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p class="text-sm font-semibold uppercase tracking-wide text-blue-700">Blog</p>
        <h1 class="mt-2 page-title">技术博客</h1>
        <p class="mt-3 max-w-2xl text-base leading-7 text-slate-600">
          记录开发实践、项目复盘和技术思考。文章内容由 Django REST Framework 提供，Markdown 在前端渲染。
        </p>
      </div>
      <p class="text-sm font-semibold text-slate-500">{{ publishedPosts.length }} 篇文章</p>
    </header>

    <div v-if="loading" class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3" aria-label="正在加载文章">
      <div v-for="index in 6" :key="index" class="page-panel animate-pulse">
        <div class="h-5 w-2/3 rounded bg-slate-200"></div>
        <div class="mt-4 h-4 w-full rounded bg-slate-200"></div>
        <div class="mt-2 h-4 w-4/5 rounded bg-slate-200"></div>
        <div class="mt-6 h-4 w-1/3 rounded bg-slate-200"></div>
      </div>
    </div>

    <div v-else-if="error" class="page-panel border-red-200 bg-red-50 text-red-800">
      {{ error }}
    </div>

    <div v-else-if="publishedPosts.length" class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <article
        v-for="post in publishedPosts"
        :key="post.id"
        class="group flex min-h-72 flex-col rounded-lg border border-slate-200 bg-white p-5 transition-colors duration-200 hover:border-blue-300 hover:bg-blue-50/40"
      >
        <div class="flex flex-wrap items-center gap-2 text-xs font-semibold text-slate-500">
          <time :datetime="post.published_at || post.created_at">
            {{ formatDate(post.published_at || post.created_at) }}
          </time>
          <span v-if="post.category" class="rounded-full bg-slate-100 px-2.5 py-1 text-slate-700">
            {{ post.category.name }}
          </span>
        </div>

        <RouterLink
          :to="{ name: 'BlogDetail', params: { id: post.id } }"
          class="mt-4 text-xl font-bold leading-snug text-slate-950 transition-colors duration-200 hover:text-blue-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600"
        >
          {{ post.title }}
        </RouterLink>

        <p class="mt-3 line-clamp-4 flex-1 text-sm leading-6 text-slate-600">
          {{ post.excerpt || '这篇文章暂时没有摘要。' }}
        </p>

        <div v-if="post.tags?.length" class="mt-5 flex flex-wrap gap-2">
          <span
            v-for="tag in post.tags"
            :key="tag.id"
            class="rounded-full border border-blue-100 bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700"
          >
            # {{ tag.name }}
          </span>
        </div>

        <RouterLink
          :to="{ name: 'BlogDetail', params: { id: post.id } }"
          class="mt-6 inline-flex min-h-11 items-center text-sm font-bold text-blue-700 transition-colors duration-200 hover:text-blue-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600"
        >
          阅读全文
        </RouterLink>
      </article>
    </div>

    <div v-else class="page-panel text-slate-600">
      暂无已发布文章。你可以先在 Django 后台创建文章并设置为 Published。
    </div>
  </section>
</template>
