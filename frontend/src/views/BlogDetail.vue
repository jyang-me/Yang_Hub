<script setup>
import DOMPurify from 'dompurify'
import hljs from 'highlight.js/lib/core'
import bash from 'highlight.js/lib/languages/bash'
import css from 'highlight.js/lib/languages/css'
import javascript from 'highlight.js/lib/languages/javascript'
import json from 'highlight.js/lib/languages/json'
import python from 'highlight.js/lib/languages/python'
import xml from 'highlight.js/lib/languages/xml'
import 'highlight.js/styles/github-dark.css'
import MarkdownIt from 'markdown-it'
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'

import request from '../api/request'

hljs.registerLanguage('bash', bash)
hljs.registerLanguage('css', css)
hljs.registerLanguage('html', xml)
hljs.registerLanguage('javascript', javascript)
hljs.registerLanguage('js', javascript)
hljs.registerLanguage('json', json)
hljs.registerLanguage('python', python)
hljs.registerLanguage('py', python)
hljs.registerLanguage('xml', xml)

const props = defineProps({
  id: {
    type: [String, Number],
    required: true,
  },
})

const markdown = new MarkdownIt({
  html: false,
  linkify: true,
  typographer: true,
  breaks: true,
  highlight(code, language) {
    const lang = language && hljs.getLanguage(language) ? language : 'plaintext'
    const highlighted = hljs.highlight(code, { language: lang, ignoreIllegals: true }).value
    return `<pre class="hljs"><code class="language-${lang}">${highlighted}</code></pre>`
  },
})

const post = ref(null)
const loading = ref(false)
const error = ref('')

const renderedContent = computed(() => {
  if (!post.value?.content) {
    return ''
  }

  const html = markdown.render(post.value.content)
  return DOMPurify.sanitize(html, {
    USE_PROFILES: { html: true },
    ADD_ATTR: ['class'],
  })
})

const categoryName = computed(() => {
  if (!post.value?.category || typeof post.value.category !== 'object') {
    return ''
  }

  return post.value.category.name
})

const tagList = computed(() => (Array.isArray(post.value?.tags) ? post.value.tags : []))

function normalizeList(payload) {
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
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value))
}

async function fetchPostByIdFallback(id) {
  const listResponse = await request.get('/posts/')
  const posts = normalizeList(listResponse.data)
  const matchedPost = posts.find((item) => String(item.id) === String(id))

  if (!matchedPost?.slug) {
    throw new Error('Post not found')
  }

  const detailResponse = await request.get(`/posts/${matchedPost.slug}/`)
  return detailResponse.data
}

async function fetchPost() {
  loading.value = true
  error.value = ''
  post.value = null

  try {
    const response = await request.get(`/posts/${props.id}/`)
    post.value = response.data
  } catch (err) {
    try {
      post.value = await fetchPostByIdFallback(props.id)
    } catch (fallbackError) {
      error.value = '文章详情加载失败，请确认文章是否存在或已经发布。'
      console.error('Failed to fetch post:', err, fallbackError)
    }
  } finally {
    loading.value = false
  }
}

onMounted(fetchPost)
watch(() => props.id, fetchPost)
</script>

<template>
  <article class="mx-auto max-w-3xl">
    <RouterLink
      to="/blog"
      class="inline-flex min-h-11 items-center text-sm font-bold text-blue-700 transition-colors duration-200 hover:text-blue-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600"
    >
      返回博客列表
    </RouterLink>

    <div v-if="loading" class="mt-6 page-panel animate-pulse" aria-label="正在加载文章详情">
      <div class="h-8 w-4/5 rounded bg-slate-200"></div>
      <div class="mt-4 h-4 w-2/5 rounded bg-slate-200"></div>
      <div class="mt-8 space-y-3">
        <div class="h-4 rounded bg-slate-200"></div>
        <div class="h-4 rounded bg-slate-200"></div>
        <div class="h-4 w-3/4 rounded bg-slate-200"></div>
      </div>
    </div>

    <div v-else-if="error" class="mt-6 page-panel border-red-200 bg-red-50 text-red-800">
      {{ error }}
    </div>

    <template v-else-if="post">
      <header class="mt-6 border-b border-slate-200 pb-8">
        <div class="flex flex-wrap items-center gap-2 text-sm font-semibold text-slate-500">
          <time :datetime="post.published_at || post.created_at">
            {{ formatDate(post.published_at || post.created_at) }}
          </time>
          <span v-if="categoryName" class="rounded-full bg-slate-100 px-2.5 py-1 text-slate-700">
            {{ categoryName }}
          </span>
        </div>

        <h1 class="mt-4 text-3xl font-bold leading-tight tracking-normal text-slate-950 sm:text-4xl">
          {{ post.title }}
        </h1>

        <p v-if="post.excerpt" class="mt-4 text-lg leading-8 text-slate-600">
          {{ post.excerpt }}
        </p>

        <div v-if="tagList.length" class="mt-5 flex flex-wrap gap-2">
          <span
            v-for="tag in tagList"
            :key="tag.id"
            class="rounded-full border border-blue-100 bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700"
          >
            # {{ tag.name }}
          </span>
        </div>
      </header>

      <div v-if="renderedContent" class="markdown-body mt-8" v-html="renderedContent"></div>
      <p v-else class="mt-8 text-slate-600">这篇文章暂时没有正文内容。</p>
    </template>
  </article>
</template>
