<template>
  <nav class="flex justify-between items-center px-6 py-4 bg-white shadow outline-none select-none">
    <div class="flex items-center space-x-2">
      <router-link to="/">
        <img src="/logo.png" alt="로고" class="w-70 h-12" />
      </router-link>
    </div>
    <div class="flex items-center space-x-6">
      <router-link to="/recommend" class="nav-link">도서 추천</router-link>
      <router-link to="/theme-books" class="nav-link">테마별 도서</router-link>
      <router-link to="/reviews" class="nav-link">모두의 감상평</router-link>
      <router-link to="/open-ending" class="nav-link">열린 결말</router-link>
      <template v-if="isLoggedIn">
        <router-link to="/mypage" class="text-sm text-gray-800">마이페이지</router-link>
        <button @click="logout" class="bg-gray-300 text-black px-4 py-1 rounded">로그아웃</button>
      </template>
      <template v-else>
        <router-link to="/signup" class="text-sm text-gray-800">회원가입</router-link>
        <router-link to="/login" class="bg-black text-white px-4 py-1 rounded">로그인</router-link>
      </template>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
console.log('🧠 userStore 상태:', userStore.user)
const isLoggedIn = computed(() => !!userStore.user?.username)

function logout() {
  localStorage.removeItem('auth_token')
  delete axios.defaults.headers.common['Authorization']
  userStore.clearUser()
  router.push('/login')
}
</script>

<style scoped>
.nav-link {
  @apply text-gray-700 hover:underline text-sm;
}
</style>
