// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import SignupPage from '@/views/SignupPage.vue'
import LoginPage from '@/views/LoginPage.vue'
// GoogleCallback import is no longer needed as the component and route will be removed.

import HomePage from '@/views/HomePage.vue'
import BookDetailPage from '@/views/BookDetailPage.vue' // 새로운 BookDetailPage 임포트

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage,
  },
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
    path: '/books/:id', // 책 ID를 파라미터로 받는 동적 라우트
    name: 'BookDetail',
    component: BookDetailPage,
    props: true // 라우트 파라미터를 props로 컴포넌트에 전달
  },
  // Removed /naver/callback and /google/callback routes as they are no longer used
  // with the django-allauth flow.
  // 앞으로 다른 경로들도 여기에 추가 가능 (예: login, home 등)
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
