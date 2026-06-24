<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import { getAssetUrl } from '../api/assets'
import request from '../api/request'

const projects = ref([])
const loading = ref(false)
const error = ref('')

const projectCount = computed(() => projects.value.length)

function normalizeList(payload) {
  return Array.isArray(payload) ? payload : payload.results || []
}

function getProjectRouteParam(project) {
  return project.slug || project.id
}

function getImageUrl(project) {
  return getAssetUrl(project.cover_image)
}

function getTechTags(project) {
  if (!project.tech_stack) {
    return []
  }

  return project.tech_stack
    .split(/[\/,，、]/)
    .map((tag) => tag.trim())
    .filter(Boolean)
}

async function fetchProjects() {
  loading.value = true
  error.value = ''

  try {
    const response = await request.get('/projects/')
    projects.value = normalizeList(response.data)
  } catch (err) {
    error.value = '项目数据加载失败，请稍后重试。'
    console.error('Failed to fetch projects:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchProjects)
</script>

<template>
  <section class="space-y-8">
    <header class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
      <div>
        <p class="text-sm font-semibold uppercase tracking-wide text-blue-700">Projects</p>
        <h1 class="mt-2 page-title">项目作品</h1>
        <p class="mt-3 max-w-2xl text-base leading-7 text-slate-600">
          这里展示从 Django REST Framework 后端接口异步获取的项目作品，包括图片、简介、技术栈和源码链接。
        </p>
      </div>
      <div class="flex items-center gap-3">
        <p class="text-sm font-semibold text-slate-500">{{ projectCount }} 个项目</p>
        <button
          type="button"
          class="inline-flex min-h-10 items-center rounded-md border border-slate-200 px-3 text-sm font-bold text-slate-700 transition-colors duration-200 hover:bg-slate-100"
          @click="fetchProjects"
        >
          刷新
        </button>
      </div>
    </header>

    <div v-if="loading" class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3" aria-label="正在加载项目">
      <article v-for="index in 6" :key="index" class="overflow-hidden rounded-lg border border-slate-200 bg-white">
        <div class="aspect-video animate-pulse bg-slate-200"></div>
        <div class="space-y-4 p-5">
          <div class="h-5 w-2/3 animate-pulse rounded bg-slate-200"></div>
          <div class="space-y-2">
            <div class="h-4 animate-pulse rounded bg-slate-200"></div>
            <div class="h-4 w-5/6 animate-pulse rounded bg-slate-200"></div>
          </div>
        </div>
      </article>
    </div>

    <div v-else-if="error" class="page-panel border-red-200 bg-red-50 text-red-800">
      {{ error }}
    </div>

    <div v-else-if="projects.length" class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <article
        v-for="project in projects"
        :key="project.id"
        class="flex overflow-hidden rounded-lg border border-slate-200 bg-white transition-colors duration-200 hover:border-blue-300 hover:bg-blue-50/40"
      >
        <div class="flex w-full flex-col">
          <RouterLink
            :to="{ name: 'ProjectDetail', params: { id: getProjectRouteParam(project) } }"
            class="block focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600"
          >
            <img
              v-if="getImageUrl(project)"
              :src="getImageUrl(project)"
              :alt="`${project.title} 项目截图`"
              class="aspect-video w-full object-cover"
              loading="lazy"
            />
            <div
              v-else
              class="flex aspect-video w-full items-center justify-center bg-slate-100 text-sm font-semibold text-slate-500"
            >
              暂无项目封面
            </div>
          </RouterLink>

          <div class="flex flex-1 flex-col p-5">
            <RouterLink
              :to="{ name: 'ProjectDetail', params: { id: getProjectRouteParam(project) } }"
              class="text-xl font-bold leading-snug text-slate-950 transition-colors duration-200 hover:text-blue-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600"
            >
              {{ project.title }}
            </RouterLink>

            <p class="mt-3 line-clamp-5 flex-1 text-sm leading-6 text-slate-600">
              {{ project.summary || project.description || '这个项目暂时没有简介。' }}
            </p>

            <div v-if="getTechTags(project).length" class="mt-5 flex flex-wrap gap-2">
              <span
                v-for="tag in getTechTags(project)"
                :key="`${project.id}-${tag}`"
                class="rounded-full border border-blue-100 bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700"
              >
                {{ tag }}
              </span>
            </div>

            <div class="mt-6 flex flex-wrap gap-3">
              <RouterLink
                :to="{ name: 'ProjectDetail', params: { id: getProjectRouteParam(project) } }"
                class="inline-flex min-h-11 items-center rounded-md bg-blue-600 px-4 text-sm font-bold text-white transition-colors duration-200 hover:bg-blue-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600"
              >
                查看详情
              </RouterLink>

              <a
                v-if="project.source_url"
                :href="project.source_url"
                target="_blank"
                rel="noreferrer"
                class="inline-flex min-h-11 items-center rounded-md bg-slate-950 px-4 text-sm font-bold text-white transition-colors duration-200 hover:bg-slate-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600"
              >
                GitHub
              </a>
            </div>
          </div>
        </div>
      </article>
    </div>

    <div v-else class="page-panel text-slate-600">
      暂无项目。你可以在 Django 后台添加 Project 数据后刷新页面。
    </div>
  </section>
</template>
