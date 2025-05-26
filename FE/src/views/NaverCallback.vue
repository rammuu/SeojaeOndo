<template>
  <div class="flex justify-center items-center min-h-screen">
    <p class="text-lg font-semibold">네이버 로그인 처리 중입니다...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

onMounted(async () => {
  const route = useRoute()
  const router = useRouter()

  const code = route.query.code
  const state = route.query.state

  if (!code || !state) {
    alert('네이버 로그인 실패: code 또는 state 누락')
    return router.push('/login')
  }

  try {
    const res = await axios.post('http://127.0.0.1:8000/api/auth/naver/', { code, state })
    const token = res.data.token
    if (token) {
      localStorage.setItem('auth_token', token)
      router.push(`/social-login/callback?token=${token}`)
    } else {
      alert('서버로부터 리디렉션 주소를 받지 못했습니다.')
      router.push('/login')
    }
  } catch (error) {
    console.error('네이버 로그인 처리 실패:', error)
    alert('네이버 로그인 중 오류가 발생했습니다.')
    router.push('/login')
  }
})
</script>
