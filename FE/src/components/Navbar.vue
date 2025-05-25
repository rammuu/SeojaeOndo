<template>
  <nav class="flex justify-between items-center px-6 py-4 bg-white shadow outline-none select-none">
    <div class="flex items-center space-x-2">
      <img src="/logo.png" alt="로고" class="w-70 h-12" />
    </div>
    <div class="flex items-center space-x-6">
      <a href="#" class="nav-link">도서 추천</a>
      <a href="#" class="nav-link">테마별 도서</a>
      <a href="#" class="nav-link">모두의 감상평</a>
      <a href="#" class="nav-link">열린 결말</a>
      <router-link to="/signup" class="text-sm text-gray-800">회원가입</router-link>
      <router-link to="/login" class="bg-black text-white px-4 py-1 rounded">로그인</router-link>
    </div>
  </nav>
</template>

<style scoped>
.nav-link {
  @apply text-gray-700 hover:underline text-sm;
}
</style>
