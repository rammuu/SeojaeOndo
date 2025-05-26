<template>
  <div class="flex justify-center items-center h-screen">
    <div class="text-center">
      <p class="text-xl font-bold mb-4">로그인 처리 중입니다...</p>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { onMounted } from 'vue'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useUserStore()

onMounted(async () => {
  const token = route.query.token
  if (!token) {
    alert('소셜 로그인 실패: 토큰이 없습니다.')
    return router.push('/login')
  }

  // 토큰 저장
  localStorage.setItem('auth_token', token)
  axios.defaults.headers.common['Authorization'] = `Token ${token}`
  console.log('🌐 현재 경로:', window.location.href)
  console.log('📦 route.query:', route.query)
  try {
    // 사용자 정보 요청
    const res = await axios.get('http://127.0.0.1:8000/api/auth/user/')
    const user = res.data
    store.setUser(user)

    // 필요한 필드(name, nickname, phone_number)가 비어있으면 추가 입력 페이지로 이동
    if (!user.name || !user.nickname || !user.phone_number) {
      // Also check for empty strings, as some fields might be present but empty
      if (user.name === '' || user.nickname === '' || user.phone_number === '') {
        return router.push('/complete-profile')
      }
    }

    // 모든 필수 정보가 채워져 있으면 홈으로 이동
    router.push('/')
  } catch (err) {
    alert('사용자 정보를 불러오지 못했습니다.')
    router.push('/login')
  }
})
</script>
