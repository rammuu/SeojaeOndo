<template>
  <div class="max-w-lg mx-auto mt-12 p-6 bg-white shadow rounded-md">
    <h2 class="text-xl font-bold mb-4">추가 정보 입력</h2>
    <form @submit.prevent="onSubmit" class="space-y-4">
      <div>
        <label class="block font-semibold">닉네임</label>
        <input v-model="form.nickname" class="input" type="text" required />
      </div>
      <div>
        <label class="block font-semibold">연락처</label>
        <input v-model="form.phone_number" class="input" type="text" required />
      </div>
      <div>
        <label class="block font-semibold">선호 도서 카테고리</label>
        <div class="grid grid-cols-3 gap-2">
          <button
            v-for="category in categoryOptions"
            :key="category"
            type="button"
            :class="['category-btn', form.favorite_categories.includes(category) ? 'selected' : '']"
            @click="toggleCategory(category)"
          >
            {{ category }}
          </button>
        </div>
      </div>
      <button type="submit" class="submit-btn w-full">저장하고 시작하기</button>
    </form>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import axios from 'axios'

const userStore = useUserStore()
const router = useRouter()

const form = reactive({
  nickname: '',
  phone_number: '',
  favorite_categories: []
})

const categoryOptions = [
  '소설/시/희곡',
  '경제/경영',
  '자기계발',
  '인문/교양',
  '취미/실용',
  '어린이/청소년',
  '과학'
]

function toggleCategory(category) {
  const index = form.favorite_categories.indexOf(category)
  if (index === -1) {
    form.favorite_categories.push(category)
  } else {
    form.favorite_categories.splice(index, 1)
  }
}

async function onSubmit() {
  try {
    await axios.patch('http://127.0.0.1:8000/api/auth/user/', form.value, {
      headers: { Authorization: `Token ${localStorage.getItem('auth_token')}` }
    })
    alert('정보가 저장되었습니다!')
    router.push('/')
  } catch (e) {
    alert('정보 저장 실패: ' + JSON.stringify(e.response?.data || e.message))
  }
}
</script>

<style scoped>
.input {
  @apply border border-gray-300 rounded-md px-3 py-2 w-full;
}
.category-btn {
  @apply px-4 py-2 rounded-md border border-gray-300 text-sm;
}
.category-btn.selected {
  @apply bg-orange-200 border-orange-400 font-semibold;
}
.submit-btn {
  @apply bg-orange-400 hover:bg-orange-500 text-white px-4 py-2 rounded-md font-bold;
}
</style>
