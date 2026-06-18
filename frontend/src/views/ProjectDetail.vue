<script setup>
import DOMPurify from 'dompurify'
import MarkdownIt from 'markdown-it'
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink } from 'vue-router'

import request from '../api/request'

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
})

const project = ref(null)
const loading = ref(false)
const error = ref('')

const renderedDescription = computed(() => {
  if (!project.value?.description) {
    return ''
  }

  return DOMPurify.sanitize(markdown.render(project.value.description), {
    USE_PROFILES: { html: true },
  })
})

const techTags = computed(() => {
  if (!project.value?.tech_stack) {
    return []
  }

  return project.value.tech_stack
    .split(/[\/,，、|]/)
    .map((tag) => tag.trim())
    .filter(Boolean)
})

function getImageUrl(projectData) {
  if (!projectData?.cover_image) {
    return ''
  }

  if (projectData.cover_image.startsWith('http')) {
    return projectData.cover_image
  }

  return `http://127.0.0.1:8000${projectData.cover_image}`
}

async function fetchProject() {
  loading.value = true
  error.value = ''
  project.value = null

  try {
    const response = await request.get(`/projects/${props.id}/`)
    project.value = response.data
  } catch (err) {
    error.value = '项目详情加载失败，请确认项目是否存在。'
    console.error('Failed to fetch project:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchProject)
watch(() => props.id, fetchProject)
</script>

<template>
  <article class="mx-auto max-w-4xl">
    <RouterLink
      to="/projects"
      class="inline-flex min-h-11 items-center text-sm font-bold text-blue-700 transition-colors duration-200 hover:text-blue-900 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600"
    >
      返回项目列表
    </RouterLink>

    <div v-if="loading" class="mt-6 overflow-hidden rounded-lg border border-slate-200 bg-white">
      <div class="aspect-video animate-pulse bg-slate-200"></div>
      <div class="space-y-4 p-6">
        <div class="h-8 w-3/4 animate-pulse rounded bg-slate-200"></div>
        <div class="h-4 w-full animate-pulse rounded bg-slate-200"></div>
        <div class="h-4 w-5/6 animate-pulse rounded bg-slate-200"></div>
      </div>
    </div>

    <div v-else-if="error" class="mt-6 page-panel border-red-200 bg-red-50 text-red-800">
      {{ error }}
    </div>

    <template v-else-if="project">
      <header class="mt-6 overflow-hidden rounded-lg border border-slate-200 bg-white">
        <img
          v-if="getImageUrl(project)"
          :src="getImageUrl(project)"
          :alt="`${project.title} 项目截图`"
          class="aspect-video w-full object-cover"
        />
        <div
          v-else
          class="flex aspect-video w-full items-center justify-center bg-slate-100 text-sm font-semibold text-slate-500"
        >
          暂无项目封面
        </div>

        <div class="p-6">
          <h1 class="text-3xl font-bold leading-tight tracking-normal text-slate-950 sm:text-4xl">
            {{ project.title }}
          </h1>

          <p v-if="project.summary" class="mt-4 text-lg leading-8 text-slate-600">
            {{ project.summary }}
          </p>

          <div v-if="techTags.length" class="mt-5 flex flex-wrap gap-2">
            <span
              v-for="tag in techTags"
              :key="tag"
              class="rounded-full border border-blue-100 bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700"
            >
              {{ tag }}
            </span>
          </div>

          <div class="mt-6 flex flex-wrap gap-3">
            <a
              v-if="project.source_url"
              :href="project.source_url"
              target="_blank"
              rel="noreferrer"
              class="inline-flex min-h-11 items-center rounded-md bg-slate-950 px-4 text-sm font-bold text-white transition-colors duration-200 hover:bg-slate-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600"
            >
              GitHub
            </a>
            <a
              v-if="project.demo_url"
              :href="project.demo_url"
              target="_blank"
              rel="noreferrer"
              class="inline-flex min-h-11 items-center rounded-md border border-blue-200 px-4 text-sm font-bold text-blue-700 transition-colors duration-200 hover:bg-blue-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600"
            >
              在线预览
            </a>
          </div>
        </div>
      </header>

      <section class="mt-8">
        <h2 class="text-xl font-bold text-slate-950">项目介绍</h2>
        <div
          v-if="renderedDescription"
          class="markdown-body mt-4"
          v-html="renderedDescription"
        ></div>
        <p v-else class="mt-4 text-slate-600">这个项目暂时没有详细介绍。</p>
      </section>
    </template>
  </article>
</template>
