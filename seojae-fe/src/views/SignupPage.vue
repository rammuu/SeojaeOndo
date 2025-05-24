<template>
  <div class="w-full max-w-xl mx-auto mt-10 p-8 bg-white shadow-xl rounded-2xl">
    <h1 class="text-2xl font-bold mb-6">회원가입</h1>

    <form @submit.prevent="onSubmit">
      <!-- 아이디 -->
      <div class="mb-4">
        <label class="block font-semibold">아이디</label>
        <div class="flex gap-2">
          <input v-model="form.username" class="input" type="text" required />
          <button class="btn" type="button" @click="checkUsernameDup">중복확인</button>
        </div>
      </div>

      <!-- 비밀번호 -->
      <div class="mb-4">
        <label class="block font-semibold">비밀번호</label>
        <input v-model="form.password1" class="input" type="password" required />
      </div>

      <!-- 비밀번호 확인 -->
      <div class="mb-4">
        <label class="block font-semibold">비밀번호 확인</label>
        <input v-model="form.password2" class="input" type="password" required />
      </div>

      <!-- 이름 -->
      <div class="mb-4">
        <label class="block font-semibold">이름</label>
        <input v-model="form.name" class="input" type="text" required />
      </div>

      <!-- 닉네임 -->
      <div class="mb-4">
        <label class="block font-semibold">닉네임</label>
        <div class="flex gap-2">
          <input v-model="form.nickname" class="input" type="text" required />
          <button class="btn" type="button" @click="checkNicknameDup">중복확인</button>
        </div>
      </div>

      <!-- 연락처 -->
      <div class="mb-4">
        <label class="block font-semibold">연락처</label>
        <input v-model="form.phone_number" class="input" type="text" required />
      </div>

      <!-- 이메일 -->
      <div class="mb-4">
        <label class="block font-semibold">이메일</label>
        <input v-model="form.email" class="input" type="email" required />
      </div>

      <!-- 선호 도서 카테고리 -->
      <div class="mb-4">
        <label class="block font-semibold">선호 도서 카테고리 <span class="text-sm text-gray-400">(최대 3개)</span></label>
        <div class="flex flex-wrap gap-2 mt-2">
          <button
            v-for="cat in allCategories"
            :key="cat"
            type="button"
            @click="toggleCategory(cat)"
            :class="{
              'bg-yellow-300': form.favorite_categories.includes(cat),
              'bg-white': !form.favorite_categories.includes(cat),
              'border': true,
              'rounded-full': true,
              'px-3': true,
              'py-1': true,
              'text-sm': true,
            }"
          >
            {{ cat }}
          </button>
        </div>
      </div>

      <!-- 제출 버튼 -->
      <button class="btn w-full mt-6">회원가입</button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { checkUsername, checkNickname, registerUser } from '@/api/auth'

const form = reactive({
  username: '',
  password1: '',
  password2: '',
  name: '',
  nickname: '',
  phone_number: '',
  email: '',
  favorite_categories: [],
})

const allCategories = [
  '소설/시/희곡', '경제/경영', '자기계발', '인문/교양',
  '차/인생', '어린이/청소년', '과학'
]

function toggleCategory(category) {
  const index = form.favorite_categories.indexOf(category)
  if (index === -1 && form.favorite_categories.length < 3) {
    form.favorite_categories.push(category)
  } else if (index !== -1) {
    form.favorite_categories.splice(index, 1)
  }
}

async function onSubmit() {
  try {
    const res = await registerUser(form)
    alert('회원가입 성공!')
    console.log('응답:', res.data)
    // router.push('/login') ← 로그인 페이지로 이동
  } catch (err) {
    console.error('에러:', err.response?.data || err.message)
    alert('회원가입 실패: ' + JSON.stringify(err.response?.data))
  }
}
const usernameAvailable = ref(null)
const nicknameAvailable = ref(null)

async function checkUsernameDup() {
  if (!form.username) return alert('아이디를 입력하세요')
  const res = await checkUsername(form.username)
  usernameAvailable.value = res.data.available
  alert(res.data.available ? '사용 가능한 아이디입니다!' : '이미 존재하는 아이디입니다.')
}

async function checkNicknameDup() {
  if (!form.nickname) return alert('닉네임을 입력하세요')
  const res = await checkNickname(form.nickname)
  nicknameAvailable.value = res.data.available
  alert(res.data.available ? '사용 가능한 닉네임입니다!' : '이미 존재하는 닉네임입니다.')
}
</script>

<style scoped>
.input {
  @apply border border-gray-300 rounded-md px-3 py-2 w-full;
}
.btn {
  @apply bg-orange-300 hover:bg-orange-400 text-white px-4 py-2 rounded-md font-semibold;
}
</style>
