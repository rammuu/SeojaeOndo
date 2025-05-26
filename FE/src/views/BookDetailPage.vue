<template>
  <div class="container mx-auto p-4">
    <div v-if="book" class="book-detail">
      <h1 class="text-3xl font-bold mb-4">{{ book.title }}</h1>
      <img :src="book.cover_image_url" :alt="book.title" class="w-64 h-auto mb-4 rounded shadow-lg">
      <p class="text-gray-700 mb-2"><span class="font-semibold">저자:</span> {{ book.author }}</p>
      <p class="text-gray-700 mb-2"><span class="font-semibold">출판사:</span> {{ book.publisher }}</p>
      <p class="text-gray-700 mb-2"><span class="font-semibold">출판일:</span> {{ book.publication_date }}</p>
      <p class="text-gray-700 mb-4"><span class="font-semibold">ISBN:</span> {{ book.isbn }}</p>
      <div class="description mb-6">
        <h2 class="text-2xl font-semibold mb-2">책 소개</h2>
        <p class="text-gray-800 whitespace-pre-line">{{ book.description }}</p>
      </div>

      <div class="threads mt-8">
        <h2 class="text-2xl font-semibold mb-4">감상평 (Threads)</h2>
        <div v-if="threads.length > 0">
          <div v-for="thread in threads" :key="thread.id" class="thread-item border p-4 mb-4 rounded shadow">
            <div class="flex items-start">
              <div class="flex-grow">
                <p class="text-gray-800 mb-2">{{ thread.content }}</p>
                <p class="text-sm text-gray-500">작성자: {{ thread.user_nickname }}</p>
              </div>
              <div v-if="thread.emotion_image_url" class="ml-4">
                <img :src="thread.emotion_image_url" alt="감정 분석 결과" class="w-12 h-12">
              </div>
            </div>
          </div>
        </div>
        <div v-else>
          <p class="text-gray-600">아직 작성된 감상평이 없습니다.</p>
        </div>
      </div>
    </div>
    <div v-else-if="loading" class="text-center">
      <p class="text-xl">책 정보를 불러오는 중입니다...</p>
    </div>
    <div v-else class="text-center">
      <p class="text-xl text-red-500">책 정보를 불러오는데 실패했습니다.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from '@/api/axios'; // Django API와 통신하기 위한 axios 인스턴스

const route = useRoute();
const book = ref(null);
const threads = ref([]);
const loading = ref(true);
const error = ref(null);

const bookId = route.params.id;

onMounted(async () => {
  try {
    loading.value = true;
    // 1. 책 상세 정보 가져오기
    const bookResponse = await axios.get(`books/${bookId}/`); // '/api/' 제거
    book.value = bookResponse.data;

    // 2. 해당 책의 감상평 (threads) 목록 가져오기
    // 백엔드 API 엔드포인트가 books/${bookId}/threads/ 와 같다고 가정합니다. (baseURL에 /api/ 포함)
    // 실제 엔드포인트에 맞게 수정해야 합니다.
    const threadsResponse = await axios.get(`books/${bookId}/threads/`); // '/api/' 제거
    
    // threadsResponse.data가 배열인지 확인
    if (Array.isArray(threadsResponse.data)) {
      threads.value = threadsResponse.data.map(thread => ({
        ...thread,
        // 백엔드에서 감정 분석 결과 이미지 URL(emotion_image_url)을 우선 사용하고,
        // 없다면 emotion 필드를 기반으로 getEmotionImageUrl 함수를 호출합니다.
        emotion_image_url: thread.emotion_image_url || getEmotionImageUrl(thread.emotion || '') // thread.emotion이 undefined일 경우 빈 문자열 전달
      }));
    } else {
      console.warn('감상평 데이터가 배열 형식이 아닙니다:', threadsResponse.data);
      threads.value = []; // 빈 배열로 초기화
    }
    error.value = null;
  } catch (err) {
    console.error('데이터를 불러오는 중 오류 발생:', err);
    // 404 오류의 경우, err.response.data에 HTML 내용이 포함될 수 있으므로
    // 좀 더 사용자 친화적인 메시지를 표시하도록 수정합니다.
    if (err.response && err.response.status === 404) {
      error.value = `책(ID: ${bookId}) 또는 관련 감상평 정보를 찾을 수 없습니다. (404 Not Found)`;
    } else {
      error.value = '데이터를 불러올 수 없습니다. 서버 또는 네트워크 연결을 확인해주세요.';
    }
    book.value = null;
    threads.value = [];
  } finally {
    loading.value = false;
  }
});

// 백엔드에서 감정 문자열만 제공할 경우, 프론트엔드에서 이미지 URL로 매핑하는 함수 (예시)
function getEmotionImageUrl(emotion) {
  if (!emotion) return null;
  // 실제 이미지 경로로 수정해야 합니다.
  const emotionImageMap = {
    '기쁨': '/src/assets/emotions/happy.png',
    '슬픔': '/src/assets/emotions/sad.png',
    '분노': '/src/assets/emotions/angry.png',
    '놀람': '/src/assets/emotions/surprised.png',
    '중립': '/src/assets/emotions/neutral.png',
    // 기타 감정들...
  };
  return emotionImageMap[emotion.toLowerCase()] || '/src/assets/emotions/default.png';
}
</script>

<style scoped>
/* Tailwind CSS 클래스를 주로 사용하므로 추가적인 스타일은 필요에 따라 작성합니다. */
.book-detail {
  max-width: 800px;
  margin: 0 auto;
}

.thread-item {
  background-color: #f9f9f9;
}

.whitespace-pre-line {
  white-space: pre-line;
}
</style>
