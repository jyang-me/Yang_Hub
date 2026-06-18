import { createRouter, createWebHistory } from 'vue-router'

import BlogDetail from '../views/BlogDetail.vue'
import BlogList from '../views/BlogList.vue'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import MessageBoard from '../views/MessageBoard.vue'
import ProjectDetail from '../views/ProjectDetail.vue'
import Projects from '../views/Projects.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: '首页' },
  },
  {
    path: '/blog',
    name: 'BlogList',
    component: BlogList,
    meta: { title: '博客列表' },
  },
  {
    path: '/blog/:id',
    name: 'BlogDetail',
    component: BlogDetail,
    props: true,
    meta: { title: '博客详情' },
  },
  {
    path: '/projects',
    name: 'Projects',
    component: Projects,
    meta: { title: '项目作品' },
  },
  {
    path: '/projects/:id',
    name: 'ProjectDetail',
    component: ProjectDetail,
    props: true,
    meta: { title: '项目详情' },
  },
  {
    path: '/messages',
    name: 'MessageBoard',
    component: MessageBoard,
    meta: { title: '留言板' },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: '登录' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} - YangHub` : 'YangHub'
})

export default router
