<template>
  <div class="w-full max-w-md mx-auto mt-20 p-8 bg-white rounded-2xl shadow-lg">
    <h1 class="text-2xl font-bold mb-6 text-center">로그인</h1>

    <form @submit.prevent="onLogin">
      <!-- 아이디 -->
      <div class="mb-4">
        <label class="block font-semibold mb-1">아이디</label>
        <input v-model="form.username" class="input" type="text" required />
      </div>

      <!-- 비밀번호 -->
      <div class="mb-6">
        <label class="block font-semibold mb-1">비밀번호</label>
        <input v-model="form.password" class="input" type="password" required />
      </div>

      <!-- 로그인 버튼 -->
      <button class="btn w-full">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { loginUser } from '@/api/auth'

const router = useRouter()
const form = reactive({
  username: '',
  password: '',
})

async function onLogin() {
  try {
    const res = await loginUser(form)
    const { access, refresh } = res.data
    localStorage.setItem('access', access)
    localStorage.setItem('refresh', refresh)

    alert('로그인 성공!')
    router.push('/')  // 홈 또는 마이페이지 등으로 이동
  } catch (err) {
    console.error(err)
    alert('로그인 실패: 아이디 또는 비밀번호를 확인하세요.')
  }
}
</script>

<style scoped>
.input {
  @apply w-full border border-gray-300 rounded-md px-3 py-2;
}

.btn {
  @apply bg-orange-400 hover:bg-orange-500 text-white font-semibold py-2 px-4 rounded-md;
}
</style>
