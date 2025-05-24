// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import SignupPage from '@/views/SignupPage.vue'

const routes = [
  {
    path: '/signup',
    component: SignupPage,
  },
  // 앞으로 다른 경로들도 여기에 추가 가능 (예: login, home 등)
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
