<template>
  <div class="flex justify-center items-center h-screen">
    <p class="text-lg font-bold">Google 로그인 처리 중...</p>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import axios from 'axios'
import { onMounted } from 'vue' 

const router = useRouter()

onMounted(async () => {
  const hashParams = new URLSearchParams(window.location.hash.slice(1))
  const access_token = hashParams.get('access_token')

  if (!access_token) {
    alert('구글 로그인 실패: 토큰이 없습니다.')
    return router.push('/login')
  }

  try {
    const res = await axios.post('http://127.0.0.1:8000/api/auth/google/', {
      access_token,
      name: '임시이름',  // 추후 사용자 입력 받기
      nickname: '임시닉네임',
      phone_number: '010-0000-0000',
      favorite_categories: ['소설'],
    })

    const token = res.data.token
    localStorage.setItem('auth_token', token)
    axios.defaults.headers.common['Authorization'] = `Token ${token}`
    router.push(`/social-login/callback?token=${token}`)
  } catch (e) {
    alert('구글 로그인 처리 실패: ' + JSON.stringify(e.response?.data || e.message))
    router.push('/login')
  }
})
</script>
