<template>
  <div class="min-h-screen bg-slate-50 text-slate-900">
    <header class="border-b border-slate-200 bg-white">
      <nav class="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-4 sm:flex-row sm:items-center sm:justify-between">
        <RouterLink to="/" class="text-xl font-semibold tracking-normal text-slate-950">
          My Blog
        </RouterLink>

        <div class="flex flex-wrap gap-2 text-sm font-medium text-slate-600">
          <RouterLink class="nav-link" to="/">首页</RouterLink>
          <RouterLink class="nav-link" to="/blog">博客</RouterLink>
          <RouterLink class="nav-link" to="/projects">项目</RouterLink>
          <RouterLink class="nav-link" to="/messages">留言板</RouterLink>
          <RouterLink class="nav-link" to="/login">登录</RouterLink>
        </div>
      </nav>
    </header>

    <main class="mx-auto w-full max-w-6xl px-4 py-8">
      <RouterView />
    </main>
  </div>
</template>
