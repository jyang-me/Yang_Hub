<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

import request from '../api/request'

const identityTags = ['电子信息工程专业', '嵌入式软件开发', '边缘 AI 探索者']

const skills = [
  {
    title: '嵌入式与硬件',
    accent: 'emerald',
    description: '面向真实设备的底层控制、通信协议和实时任务调度。',
    items: ['STM32 / ESP32', 'FreeRTOS', 'RS-485 / Modbus', 'I2C / SPI'],
  },
  {
    title: '机器视觉与算法',
    accent: 'blue',
    description: '从图像处理到轻量化部署，探索边缘侧智能感知。',
    items: ['YOLO 目标检测', 'OpenCV', '模型量化', '边缘推理'],
  },
  {
    title: '全栈开发',
    accent: 'cyan',
    description: '把硬件数据、Web API 和前端体验连接成完整产品。',
    items: ['Vue 3', 'Vite', 'Django / DRF', 'FastAPI'],
  },
]

const terminalLines = [
  { prompt: '$', text: 'yanghub flash --target stm32 --port auto', color: 'text-emerald-300' },
  { prompt: 'scan', text: 'usb: st-link detected', color: 'text-slate-500' },
  { prompt: '[01]', text: 'erasing flash sector 0x08000000', color: 'text-blue-300' },
  { prompt: '[02]', text: 'writing control_loop.bin', color: 'text-blue-300' },
  { prompt: '[03]', text: 'verifying checksum 0xA7F3', color: 'text-blue-300' },
  { prompt: '[OK]', text: 'firmware booted in 248ms', color: 'text-emerald-300' },
  { prompt: '$', text: 'vision run --model yolov8-lite --edge', color: 'text-emerald-300' },
  { prompt: 'log', text: 'camera stream online / fps=31', color: 'text-cyan-300' },
  { prompt: 'log', text: 'api gateway synced with django', color: 'text-cyan-300' },
  { prompt: 'READY', text: 'modules online', color: 'text-emerald-300' },
]

const stats = ref({
  posts: 0,
  projects: 0,
  messages: 0,
})
const statsLoading = ref(false)

const posts = ref([])
const projects = ref([])
const loadingUpdates = ref(false)

const typedText = ref('')
const tagIndex = ref(0)
const charIndex = ref(0)
const deleting = ref(false)
let typewriterTimer = null

const statItems = computed(() => [
  { label: '博客文章', value: stats.value.posts },
  { label: '开源项目', value: stats.value.projects },
  { label: '累计留言', value: stats.value.messages },
])

const recentUpdates = computed(() => {
  const recentPosts = posts.value.slice(0, 3).map((post) => ({
    id: `post-${post.id}`,
    label: '博客',
    title: post.title,
    subtitle: post.excerpt || '新的技术记录已发布',
    to: { name: 'BlogDetail', params: { id: post.slug || post.id } },
    time: post.published_at || post.created_at,
  }))

  const recentProjects = projects.value.slice(0, 2).map((project) => ({
    id: `project-${project.id}`,
    label: '项目',
    title: project.title,
    subtitle: project.summary || '新的项目作品已上线',
    to: { name: 'ProjectDetail', params: { id: project.slug || project.id } },
    time: project.created_at,
  }))

  return [...recentPosts, ...recentProjects]
    .sort((a, b) => new Date(b.time || 0) - new Date(a.time || 0))
    .slice(0, 3)
})

function normalizeList(payload) {
  return Array.isArray(payload) ? payload : payload.results || []
}

function formatDate(value) {
  if (!value) {
    return '最近'
  }

  return new Intl.DateTimeFormat('zh-CN', {
    month: 'short',
    day: 'numeric',
  }).format(new Date(value))
}

function runTypewriter() {
  const currentTag = identityTags[tagIndex.value]

  if (!deleting.value) {
    typedText.value = currentTag.slice(0, charIndex.value + 1)
    charIndex.value += 1

    if (charIndex.value === currentTag.length) {
      deleting.value = true
      typewriterTimer = window.setTimeout(runTypewriter, 1300)
      return
    }
  } else {
    typedText.value = currentTag.slice(0, charIndex.value - 1)
    charIndex.value -= 1

    if (charIndex.value === 0) {
      deleting.value = false
      tagIndex.value = (tagIndex.value + 1) % identityTags.length
    }
  }

  typewriterTimer = window.setTimeout(runTypewriter, deleting.value ? 42 : 88)
}

async function fetchStats() {
  statsLoading.value = true

  try {
    const response = await request.get('/stats/')
    stats.value = {
      posts: response.data.posts_count ?? response.data.posts ?? 0,
      projects: response.data.projects_count ?? response.data.projects ?? 0,
      messages: response.data.messages_count ?? response.data.messages ?? 0,
    }
  } catch {
    const [postsResult, projectsResult] = await Promise.allSettled([
      request.get('/posts/'),
      request.get('/projects/'),
    ])

    const postList =
      postsResult.status === 'fulfilled' ? normalizeList(postsResult.value.data) : []
    const projectList =
      projectsResult.status === 'fulfilled' ? normalizeList(projectsResult.value.data) : []

    stats.value = {
      posts: postList.length,
      projects: projectList.length,
      messages: 0,
    }
  } finally {
    statsLoading.value = false
  }
}

async function fetchRecentUpdates() {
  loadingUpdates.value = true

  try {
    const [postsResponse, projectsResponse] = await Promise.all([
      request.get('/posts/'),
      request.get('/projects/'),
    ])
    posts.value = normalizeList(postsResponse.data)
    projects.value = normalizeList(projectsResponse.data)
  } catch (error) {
    console.error('Failed to fetch recent updates:', error)
  } finally {
    loadingUpdates.value = false
  }
}

onMounted(() => {
  runTypewriter()
  fetchStats()
  fetchRecentUpdates()
})

onUnmounted(() => {
  if (typewriterTimer) {
    window.clearTimeout(typewriterTimer)
  }
})
</script>

<template>
  <section class="space-y-10">
    <section
      class="relative isolate overflow-hidden rounded-lg bg-slate-950 px-5 py-10 text-white sm:px-8 lg:px-10 lg:py-14"
    >
      <div class="absolute inset-0 -z-10 opacity-40">
        <div class="absolute inset-0 bg-[linear-gradient(rgba(59,130,246,0.18)_1px,transparent_1px),linear-gradient(90deg,rgba(59,130,246,0.18)_1px,transparent_1px)] bg-[size:36px_36px]"></div>
        <div class="absolute inset-x-0 top-0 h-64 bg-blue-500/20 blur-3xl"></div>
        <div class="absolute bottom-0 right-0 h-72 w-72 bg-emerald-400/20 blur-3xl"></div>
      </div>

      <div class="grid items-center gap-10 lg:grid-cols-[1.05fr_0.95fr]">
        <div>
          <p class="text-sm font-bold uppercase tracking-[0.24em] text-emerald-300">
            YangHub / Lab Notes / Open Source
          </p>

          <h1 class="mt-5 max-w-3xl text-4xl font-black leading-tight tracking-normal text-white sm:text-5xl lg:text-6xl">
            让嵌入式智能
            <span class="block text-blue-400">驱动云端应用生长</span>
          </h1>

          <div class="mt-6 min-h-12 rounded-md border border-white/10 bg-white/5 px-4 py-3 font-mono text-base text-slate-200 sm:text-lg">
            <span class="text-emerald-300">identity:</span>
            <span class="ml-2 text-white">{{ typedText }}</span>
            <span class="ml-1 inline-block h-5 w-2 translate-y-1 animate-pulse bg-blue-400"></span>
          </div>

          <p class="mt-6 max-w-2xl text-base leading-8 text-slate-300">
            我关注嵌入式控制、机器视觉、边缘 AI 与全栈工程实践。这里沉淀项目复盘、技术博客和可持续迭代的开源作品
          </p>

          <div class="mt-8 flex flex-col gap-3 sm:flex-row">
            <RouterLink
              to="/blog"
              class="inline-flex min-h-12 items-center justify-center rounded-md bg-blue-500 px-5 text-sm font-bold text-white shadow-lg shadow-blue-500/25 transition-colors duration-200 hover:bg-blue-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-300"
            >
              浏览技术博客
            </RouterLink>
            <RouterLink
              to="/projects"
              class="inline-flex min-h-12 items-center justify-center rounded-md border border-emerald-300/60 px-5 text-sm font-bold text-emerald-200 transition-colors duration-200 hover:bg-emerald-300 hover:text-slate-950 focus-visible:outline focus-visible:outline-2 focus-visible:outline-emerald-300"
            >
              开源项目作品
            </RouterLink>
          </div>
        </div>

        <div class="relative">
          <div class="rounded-lg border border-white/10 bg-slate-900/80 p-5 shadow-2xl shadow-blue-950/50 backdrop-blur">
            <div class="flex items-center gap-2 border-b border-white/10 pb-4">
              <span class="h-3 w-3 rounded-full bg-red-400"></span>
              <span class="h-3 w-3 rounded-full bg-yellow-300"></span>
              <span class="h-3 w-3 rounded-full bg-emerald-400"></span>
              <span class="ml-3 text-xs font-semibold text-slate-400">yanghub@edge-node:~</span>
            </div>

            <div class="terminal-panel mt-5 rounded-md border border-slate-700/80 bg-slate-950/90 p-4 font-mono text-xs text-slate-300 shadow-inner shadow-blue-950/60 sm:text-sm">
              <div class="mb-4 flex items-center justify-between border-b border-slate-800 pb-3">
                <span class="text-slate-500">flash-session.log</span>
                <span class="flex items-center gap-2 text-emerald-300">
                  <span class="h-2 w-2 animate-pulse rounded-full bg-emerald-400"></span>
                  running
                </span>
              </div>

              <div class="terminal-stream h-80 overflow-hidden leading-6">
                <p
                  v-for="line in terminalLines"
                  :key="`${line.prompt}-${line.text}`"
                  class="terminal-line"
                >
                  <span :class="line.color">{{ line.prompt }}</span>
                  <span class="ml-2">{{ line.text }}</span>
                  <span
                    v-if="line.prompt === 'READY'"
                    class="terminal-cursor ml-1 inline-block h-4 w-2 translate-y-0.5 bg-emerald-300"
                  ></span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="grid gap-4 rounded-lg border border-slate-200 bg-white p-5 shadow-sm sm:grid-cols-3">
      <div
        v-for="item in statItems"
        :key="item.label"
        class="rounded-md border border-slate-200 bg-slate-50 p-5"
      >
        <p class="text-sm font-semibold text-slate-500">{{ item.label }}</p>
        <p class="mt-2 text-3xl font-black text-slate-950">
          <span v-if="statsLoading" class="inline-block h-8 w-16 animate-pulse rounded bg-slate-200"></span>
          <span v-else>{{ item.value }}</span>
        </p>
      </div>
    </section>

    <section>
      <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p class="text-sm font-bold uppercase tracking-[0.2em] text-blue-700">Skills Matrix</p>
          <h2 class="mt-2 text-2xl font-black text-slate-950">核心技能树</h2>
        </div>
        <p class="max-w-xl text-sm leading-6 text-slate-600">
          从 MCU 到 Web API，再到边缘智能部署，技术栈围绕“能落地的系统”组织。
        </p>
      </div>

      <div class="mt-6 grid gap-5 md:grid-cols-3">
        <article
          v-for="skill in skills"
          :key="skill.title"
          class="rounded-lg border border-slate-200 bg-white p-5 shadow-sm transition duration-200 hover:scale-105 hover:border-blue-300 hover:shadow-xl hover:shadow-blue-100"
        >
          <div
            class="mb-5 h-1.5 w-20 rounded-full"
            :class="{
              'bg-emerald-400': skill.accent === 'emerald',
              'bg-blue-500': skill.accent === 'blue',
              'bg-cyan-400': skill.accent === 'cyan',
            }"
          ></div>
          <h3 class="text-xl font-black text-slate-950">{{ skill.title }}</h3>
          <p class="mt-3 min-h-16 text-sm leading-6 text-slate-600">{{ skill.description }}</p>
          <div class="mt-5 flex flex-wrap gap-2">
            <span
              v-for="item in skill.items"
              :key="item"
              class="rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-xs font-bold text-slate-700"
            >
              {{ item }}
            </span>
          </div>
        </article>
      </div>
    </section>

    <section class="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
      <div class="rounded-lg border border-slate-200 bg-white p-6">
        <p class="text-sm font-bold uppercase tracking-[0.2em] text-emerald-700">Build Log</p>
        <h2 class="mt-2 text-2xl font-black text-slate-950">工程方法</h2>
        <div class="mt-6 space-y-4 text-sm leading-7 text-slate-600">
          <p>先让硬件稳定，再让算法可靠，最后把数据和交互放进可维护的产品界面。</p>
          <p>关注清晰的模块边界、可复用接口、可观测的运行状态，以及能被长期迭代的项目结构。</p>
        </div>
      </div>

      <div class="rounded-lg border border-slate-200 bg-white p-6">
        <div class="flex items-center justify-between gap-4">
          <div>
            <p class="text-sm font-bold uppercase tracking-[0.2em] text-blue-700">Recent Updates</p>
            <h2 class="mt-2 text-2xl font-black text-slate-950">最近动态</h2>
          </div>
          <RouterLink to="/blog" class="text-sm font-bold text-blue-700 hover:text-blue-900">
            查看全部
          </RouterLink>
        </div>

        <div v-if="loadingUpdates" class="mt-6 space-y-4">
          <div v-for="index in 3" :key="index" class="h-16 animate-pulse rounded-md bg-slate-100"></div>
        </div>

        <ol v-else-if="recentUpdates.length" class="mt-6 space-y-5">
          <li v-for="update in recentUpdates" :key="update.id" class="relative border-l border-slate-200 pl-5">
            <span class="absolute -left-1.5 top-1.5 h-3 w-3 rounded-full bg-blue-500"></span>
            <div class="flex flex-wrap items-center gap-2 text-xs font-bold text-slate-500">
              <span class="rounded-full bg-blue-50 px-2 py-1 text-blue-700">{{ update.label }}</span>
              <time>{{ formatDate(update.time) }}</time>
            </div>
            <RouterLink
              :to="update.to"
              class="mt-2 block text-base font-black text-slate-950 transition-colors duration-200 hover:text-blue-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-blue-600"
            >
              {{ update.title }}
            </RouterLink>
            <p class="mt-1 line-clamp-2 text-sm leading-6 text-slate-600">{{ update.subtitle }}</p>
          </li>
        </ol>

        <p v-else class="mt-6 text-sm text-slate-600">
          暂无动态。发布文章或项目后，这里会自动更新。
        </p>
      </div>
    </section>
  </section>
</template>
