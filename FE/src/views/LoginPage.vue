<template>
  <div class="flex justify-center mt-10">
    <div class="w-full max-w-sm">
      <!-- 로그인 제목 -->
      <h2 class="text-xl font-bold mb-1">로그인</h2>
      <hr class="mb-6" />

      <!-- 아이디/비밀번호 입력 -->
      <div class="mb-4">
        <label class="block text-sm mb-1">아이디</label>
        <input v-model="form.username" class="input" type="text" />
      </div>
      <div class="mb-4">
        <label class="block text-sm mb-1">비밀번호</label>
        <input v-model="form.password" class="input" type="password" />
      </div>

      <!-- 로그인 버튼 -->
      <button
        @click="onLogin"
        class="w-full bg-amber-300 hover:bg-amber-400 text-white font-semibold py-2 rounded-full"
      >
        로그인
      </button>

      <!-- 소셜 로그인 구분선 -->
      <div class="flex items-center my-6">
        <div class="flex-grow border-t"></div>
        <span class="mx-2 text-sm text-gray-500">소셜 로그인</span>
        <div class="flex-grow border-t"></div>
      </div>

      <!-- 네이버 로그인 -->
      <button @click="redirectToNaver" class="w-full h-12 bg-green-500 text-white font-semibold rounded-md mb-4">
        <span class="flex items-center justify-center">
          <img src="/naver.svg" alt="naver" class="w-5 h-5 mr-2" />
          네이버 로그인
        </span>
      </button>

      <!-- 카카오 로그인 -->
      <a :href="kakaoLoginUrl" class="w-full bg-yellow-300 text-black py-2 rounded-full font-semibold flex items-center justify-center mb-3">
        <img src="/kakao.png" alt="kakao" class="w-5 h-5 mr-2" />
        카카오 로그인
      </a>

      <!-- 구글 로그인 -->
      <a :href="googleLoginUrl" class="w-full border border-gray-500 text-gray-800 py-2 rounded-full font-semibold flex items-center justify-center">
        <img src="/google.png" alt="google" class="w-5 h-5 mr-2" />
        구글 로그인
      </a>

      <!-- 아이디 찾기 / 비밀번호 찾기 -->
      <div class="text-xs text-right mt-2 text-gray-500">
        <a href="#" class="hover:underline">아이디 찾기</a>
        /
        <a href="#" class="hover:underline">비밀번호 찾기</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const form = reactive({
  username: '',
  password: ''
})

const router = useRouter()
const userStore = useUserStore()

async function onLogin() {
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/auth/login/', {
      username: form.username,
      password: form.password
    })

    const token = response.data.key
    localStorage.setItem('authToken', token)
    userStore.setToken(token)
    userStore.setUsername(form.username)
    alert('로그인 성공')
    router.push('/')
  } catch (err) {
    alert('로그인 실패: 아이디 또는 비밀번호를 확인하세요.')
  }
}

const NAVER_CLIENT_ID = '7ERX5hjREVcs6iqwMjLp'  // 실제 값으로 바꿔주세요
const REDIRECT_URI = 'http://localhost:5173/naver/callback'

function redirectToNaver() {
  const state = Date.now().toString()  // CSRF 방지용, 간단히 timestamp 사용
  const url = `https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id=${NAVER_CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&state=${state}`
  window.location.href = url
}

const googleLoginUrl = computed(() =>
  'http://127.0.0.1:8000/accounts/google/login/?process=login'
)
const kakaoLoginUrl = computed(() =>
  'http://127.0.0.1:8000/accounts/kakao/login/?process=login'
)
const naverLoginUrl = computed(() =>
  'http://127.0.0.1:8000/accounts/naver/login/?process=login'
)
</script>

<style scoped>
.input {
  @apply border border-gray-300 rounded-md px-3 py-2 w-full;
}
</style>
