<template>
  <div class="min-h-screen bg-white outline-none select-none">

    <!-- ✅ 회원가입 폼 -->
    <div class="flex justify-center px-4">
      <div class="max-w-2xl w-full mt-12 p-8 bg-white rounded-2xl">
        <h1 class="text-2xl font-bold mb-4">회원가입</h1>
        <hr class="mb-6" />

        <form @submit.prevent="onSubmit">
          <div class="space-y-4">
            <!-- 아이디 -->
            <div class="flex items-center gap-2">
              <label class="w-1/5 font-semibold">아이디</label>
              <input v-model="form.username" class="input flex-1" type="text" required />
              <button type="button" @click="checkUsername" class="check-btn">중복검사</button>
            </div>
            <div v-if="usernameAvailable === true" class="text-green-600 text-sm ml-32">입력하신 아이디를 사용할 수 있습니다.</div>
            <div v-else-if="usernameAvailable === false" class="text-red-500 text-sm ml-32">입력하신 아이디는 이미 등록된 아이디로 사용할 수 없습니다.</div>

            <!-- 비밀번호 -->
            <div class="flex items-center gap-2">
              <label class="w-1/5 font-semibold">비밀번호</label>
              <input v-model="form.password1" class="input flex-1" type="password" required />
            </div>

            <!-- 비밀번호 확인 -->
            <div class="flex items-center gap-2">
              <label class="w-1/5 font-semibold">비밀번호 확인</label>
              <input v-model="form.password2" class="input flex-1" type="password" required />
            </div>
            <div v-if="form.password2 && form.password1 === form.password2" class="text-green-600 text-sm ml-32">비밀번호가 일치합니다.</div>
            <div v-else-if="form.password2 && form.password1 !== form.password2" class="text-red-500 text-sm ml-32">비밀번호가 일치하지 않습니다.</div>

            <!-- 이름 -->
            <div class="flex items-center gap-2">
              <label class="w-1/5 font-semibold">이름</label>
              <input v-model="form.name" class="input flex-1" type="text" required />
            </div>

            <!-- 닉네임 -->
            <div class="flex items-center gap-2">
              <label class="w-1/5 font-semibold">닉네임</label>
              <input v-model="form.nickname" class="input flex-1" type="text" required />
              <button type="button" @click="checkNickname" class="check-btn">중복검사</button>
            </div>
            <div v-if="nicknameAvailable === true" class="text-green-600 text-sm ml-32">사용 가능한 닉네임입니다.</div>
            <div v-else-if="nicknameAvailable === false" class="text-red-500 text-sm ml-32">이미 사용 중인 닉네임입니다.</div>

            <!-- 연락처 -->
            <div class="flex items-center gap-2">
              <label class="w-1/5 font-semibold">연락처</label>
              <input v-model="form.phone_number" class="input flex-1" type="text" />
            </div>

            <!-- 이메일 -->
            <div class="flex items-center gap-2">
              <label class="w-1/5 font-semibold">이메일</label>
              <input v-model="form.email" class="input flex-1" type="email" required />
            </div>

            <!-- 선호 카테고리 -->
            <div>
              <div class="font-semibold mb-1">선호 도서 카테고리 <span class="text-xs text-orange-400">(중복 선택 가능)</span></div>
              <div class="grid grid-cols-4 gap-2">
                <button v-for="category in categoryOptions" :key="category" type="button"
                        :class="{'selected': form.favorite_categories.includes(category)}"
                        @click="toggleCategory(category)"
                        class="category-btn">
                  {{ category }}
                </button>
              </div>
            </div>
          </div>

          <button class="submit-btn mt-8 w-full">회원가입</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { registerUser, checkUsernameAPI, checkNicknameAPI } from '@/api/auth'

const form = reactive({
  username: '',
  password1: '',
  password2: '',
  name: '',
  nickname: '',
  phone_number: '',
  email: '',
  favorite_categories: []
})

const usernameAvailable = ref(null)
const nicknameAvailable = ref(null)

const categoryOptions = ['소설/시/희곡', '경제/경영', '자기계발', '인문/교양', '취미/실용', '어린이/청소년', '과학']

function toggleCategory(category) {
  const index = form.favorite_categories.indexOf(category)
  if (index === -1) {
    form.favorite_categories.push(category)
  } else {
    form.favorite_categories.splice(index, 1)
  }
}

async function checkUsername() {
  try {
    const res = await checkUsernameAPI(form.username)
    usernameAvailable.value = res.data.available
  } catch {
    usernameAvailable.value = false
  }
}

async function checkNickname() {
  try {
    const res = await checkNicknameAPI(form.nickname)
    nicknameAvailable.value = res.data.available
  } catch {
    nicknameAvailable.value = false
  }
}

async function onSubmit() {
  try {
    if (form.password1 !== form.password2) {
      alert('비밀번호가 일치하지 않습니다.')
      return
    }
    if (nicknameAvailable.value !== true) {
      alert('닉네임 중복 여부를 확인해 주세요.')
      return
    }
    const res = await registerUser(form)
    const { access, refresh } = res.data
    localStorage.setItem('access', access)
    localStorage.setItem('refresh', refresh)
    alert('회원가입 완료!')
    window.location.href = '/'
  } catch (err) {
    alert('회원가입 실패: ' + JSON.stringify(err.response?.data || err.message))
  }
}
</script>

<style scoped>
.input {
  @apply border border-gray-300 rounded-md px-3 py-2 w-full;
}
.check-btn {
  @apply bg-orange-400 hover:bg-orange-400 text-white px-4 py-2 rounded-md font-semibold;
}
.category-btn {
  @apply px-4 py-2 rounded-md border border-gray-300;
}
.category-btn.selected {
  @apply bg-orange-100 border-orange-300 border-2;
}
.submit-btn {
  @apply bg-orange-400 hover:bg-orange-500 text-white px-4 py-2 rounded-md font-bold;
}
.nav-link {
  @apply text-gray-700 hover:underline text-sm;
}
</style>