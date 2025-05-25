// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import SignupPage from '@/views/SignupPage.vue'
import LoginPage from '@/views/LoginPage.vue'

const routes = [
  {
    path: '/signup',
    component: SignupPage,
  },
  { 
    path: '/login',
    component: LoginPage 
  },
  {
    path: '/social-login/callback',
    name: 'SocialLoginCallback',
    component: () => import('@/views/SocialLoginCallback.vue')
  },
  {
    path: '/complete-profile',
    name: 'CompleteProfile',
    component: () => import('@/views/CompleteProfile.vue')
  },
  {
    path: '/naver/callback',
    name: 'NaverCallback',
    component: () => import('@/views/NaverCallback.vue')
  },
  // 앞으로 다른 경로들도 여기에 추가 가능 (예: login, home 등)
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
