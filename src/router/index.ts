import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Welcome',
    component: () => import('@/views/Welcome.vue'),
    meta: { title: 'AIPPOF - 欢迎' }
  },
  {
    path: '/path-a',
    name: 'PathA',
    children: [
      {
        path: 'input',
        name: 'PathAInput',
        component: () => import('@/views/PathA/InputForm.vue'),
        meta: { title: '新参与者 - 数据输入' }
      },
      {
        path: 'report',
        name: 'PathAReport',
        component: () => import('@/views/PathA/Report.vue'),
        meta: { title: '新参与者 - AI预测报告' }
      }
    ]
  },
  {
    path: '/path-b',
    name: 'PathB',
    children: [
      {
        path: 'input',
        name: 'PathBInput',
        component: () => import('@/views/PathB/InputForm.vue'),
        meta: { title: '已参与者 - 数据输入' }
      },
      {
        path: 'report',
        name: 'PathBReport',
        component: () => import('@/views/PathB/Report.vue'),
        meta: { title: '已参与者 - 诊断报告' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫 - 更新页面标题
router.beforeEach((to, _from, next) => {
  document.title = (to.meta.title as string) || 'AIPPOF'
  next()
})

export default router
