<template>
  <div class="flex justify-center mt-10">
    <div class="w-full max-w-md">
      <h2 class="text-2xl font-bold mb-6 text-center">프로필 정보 추가 입력</h2>
      <p class="text-center text-gray-600 mb-6">
        서비스 이용을 위해 추가 정보를 입력해주세요.
      </p>
      <form @submit.prevent="updateProfile" class="space-y-6">
        <div>
          <label for="name" class="block text-sm font-medium text-gray-700 mb-1">이름</label>
          <input
            type="text"
            id="name"
            v-model="form.name"
            class="input"
            :disabled="!!userStore.user?.name"
            placeholder="이름을 입력하세요"
          />
        </div>
        <div>
          <label for="nickname" class="block text-sm font-medium text-gray-700 mb-1">닉네임</label>
          <input
            type="text"
            id="nickname"
            v-model="form.nickname"
            class="input"
            :disabled="!!userStore.user?.nickname"
            placeholder="닉네임을 입력하세요"
          />
          <!-- TODO: Add nickname availability check if needed -->
        </div>
        <div>
          <label for="phone_number" class="block text-sm font-medium text-gray-700 mb-1">전화번호</label>
          <input
            type="tel"
            id="phone_number"
            v-model="form.phone_number"
            class="input"
            :disabled="!!userStore.user?.phone_number"
            placeholder="010-1234-5678"
          />
        </div>
        <div>
          <button
            type="submit"
            class="w-full bg-amber-500 hover:bg-amber-600 text-white font-semibold py-2 px-4 rounded-md focus:outline-none focus:ring-2 focus:ring-amber-500 focus:ring-offset-2"
            :disabled="isSubmitting"
          >
            {{ isSubmitting ? '저장 중...' : '정보 저장 및 계속하기' }}
          </button>
        </div>
        <div v-if="errorMessage" class="text-red-500 text-sm text-center">
          {{ errorMessage }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import axios from 'axios'

const router = useRouter()
const userStore = useUserStore()

const form = reactive({
  name: '',
  nickname: '',
  phone_number: '',
})

const isSubmitting = ref(false)
const errorMessage = ref('')

onMounted(() => {
  if (userStore.user) {
    form.name = userStore.user.name || ''
    form.nickname = userStore.user.nickname || ''
    form.phone_number = userStore.user.phone_number || ''
  } else {
    // If no user data in store (e.g., page refresh), redirect to login
    // Or try to fetch user data again if a token exists
    if (localStorage.getItem('auth_token')) {
        axios.get('http://127.0.0.1:8000/api/auth/user/')
            .then(res => {
                userStore.setUser(res.data)
                form.name = userStore.user.name || ''
                form.nickname = userStore.user.nickname || ''
                form.phone_number = userStore.user.phone_number || ''
                if (userStore.user.name && userStore.user.nickname && userStore.user.phone_number) {
                    router.push('/') // Already complete
                }
            })
            .catch(() => router.push('/login'))
    } else {
        router.push('/login')
    }
  }
})

async function updateProfile() {
  isSubmitting.value = true
  errorMessage.value = ''

  const dataToUpdate = {}
  if (!userStore.user?.name && form.name) dataToUpdate.name = form.name
  if (!userStore.user?.nickname && form.nickname) dataToUpdate.nickname = form.nickname
  if (!userStore.user?.phone_number && form.phone_number) dataToUpdate.phone_number = form.phone_number
  
  if (Object.keys(dataToUpdate).length === 0) {
    // If all fields were already populated and disabled, or no new data entered
    router.push('/')
    isSubmitting.value = false
    return
  }

  try {
    const response = await axios.patch('http://127.0.0.1:8000/api/auth/user/', dataToUpdate)
    userStore.setUser(response.data) // Update store with latest user info
    alert('프로필 정보가 성공적으로 업데이트되었습니다.')
    router.push('/')
  } catch (err) {
    console.error('Profile update error:', err.response?.data || err.message)
    errorMessage.value = '프로필 업데이트에 실패했습니다. 입력 값을 확인해주세요.'
    if (err.response?.data) {
        // More specific error messages
        if (err.response.data.nickname) {
            errorMessage.value = `닉네임 오류: ${err.response.data.nickname.join(', ')}`
        } else if (err.response.data.phone_number) {
            errorMessage.value = `전화번호 오류: ${err.response.data.phone_number.join(', ')}`
        }
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.input {
  @apply mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-amber-500 focus:border-amber-500 sm:text-sm;
}
input:disabled {
  @apply bg-gray-100 cursor-not-allowed;
}
</style>
