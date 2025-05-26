<!-- src/views/HomePage.vue -->
<template>
  <div class="home-page">
    <div class="sections-wrapper" ref="wrapper">

      <!-- 섹션1: Hero -->
      <section id="section1" class="section hero">
        <div class="hero-content">
          <img
            class="hero-image"
            :src="heroIllustration"
            alt="hero illustration"
          />
          <div class="hero-text">
            <h1>당신의 서재는 지금 몇 도인가요?</h1>
            <p>
              AI가 당신의 감성과 취향을 이해하고 가장 어울리는 책 두 권을 추천해드립니다.<br />
              ‘선호 도서 카테고리’와 당신만의 독서 패턴을 분석한 ‘내 알고리즘’을 바탕으로<br />
              지금의 당신에게 가장 필요한 책을 연결해드려요.
            </p>
            <button class="btn-primary" @click="$router.push('/recommend')">
              바로가기
            </button>
          </div>
        </div>
        <div class="scroll-arrow" @click="scrollTo('section2')">▼</div>
      </section>

      <!-- 섹션2: 테마별 도서 + 베스트셀러 -->
      <section id="section2" class="section theme-best">
        <div class="theme-grid">
          <h2>테마별 도서</h2>
          <div
            v-for="theme in themes"
            :key="theme.id"
            class="theme-item"
            @click="$router.push(`/theme/${theme.id}`)"
          >
            <img :src="theme.icon" :alt="theme.label" />
            <span>{{ theme.label }}</span>
          </div>
        </div>

        <div class="best-seller">
          <h2>베스트 셀러</h2>
          <div class="books">
            <div class="book-card" v-for="n in 4" :key="n">
              <div class="book-thumb">이미지</div>
              <div class="book-title">제목</div>
              <div class="book-author">저자</div>
            </div>
          </div>
        </div>

        <div class="scroll-arrow" @click="scrollTo('section3')">▼</div>
      </section>

      <!-- 섹션3: 인기 감상평 + 인기 열린결말 -->
      <section id="section3" class="section popular">

        <!-- 3.1) 인기 감상평 -->
        <div class="popular-block">
          <div class="popular-content">
            <!-- 좌측 텍스트 -->
            <div class="popular-info">
              <span class="overlay-text">Hot</span>
              <h2 class="heading">인기 감상평</h2>
              <p class="subheading">
                지금 가장 인기 있는 감상평을 만나보세요!<br />
                독자들이 사랑한 생생한 리뷰를 한눈에 확인할 수 있습니다.
              </p>
              <div class="dots">
                <span class="dot active"></span>
                <span class="dot"></span>
                <span class="dot"></span>
              </div>
            </div>
            <!-- 우측 카드 -->
            <div class="popular-cards">
              <div
                class="card"
                v-for="review in popularReviews"
                :key="review.id"
              >
                <img
                  :src="review.img"
                  alt="카테고리"
                  class="card-badge"
                />
                <h3 class="quote">“{{ review.title }}”</h3>
                <p class="text">{{ review.text }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 3.2) 인기 열린결말 -->
        <div class="popular-block">
          <div class="popular-content">
            <div class="popular-info">
              <span class="overlay-text">Popular</span>
              <h2 class="heading">인기 열린결말</h2>
              <p class="subheading">
                여운을 남기는 열린 결말,<br />
                당신의 해석은 무엇인가요? 다양한 시선의 감상평을 확인해보세요.
              </p>
              <div class="dots">
                <span class="dot"></span>
                <span class="dot active"></span>
                <span class="dot"></span>
              </div>
            </div>
            <div class="popular-cards">
              <div
                class="card"
                v-for="ending in popularEndings"
                :key="ending.id"
              >
                <img
                  :src="ending.img"
                  alt="카테고리"
                  class="card-badge"
                />
                <h3 class="quote">“{{ ending.title }}”</h3>
                <p class="text">{{ ending.text }}</p>
              </div>
            </div>
          </div>
        </div>

      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

// Hero 일러스트
import heroIllustration from '@/assets/hero-illustration.png'

// 테마 아이콘
import iconNovel      from '@/assets/icons/novel.png'
import iconBusiness   from '@/assets/icons/business.png'
import iconSelf       from '@/assets/icons/self.png'
import iconHumanities from '@/assets/icons/humanities.png'
import iconHobby      from '@/assets/icons/hobby.png'
import iconKids       from '@/assets/icons/kids.png'
import iconScience    from '@/assets/icons/science.png'

// 카드 상단 원형 이미지
import novelCircle      from '@/assets/circles/novel_circle.png'
import businessCircle   from '@/assets/circles/business_circle.png'
import selfCircle       from '@/assets/circles/self_circle.png'
import humanitiesCircle from '@/assets/circles/humanities_circle.png'
import hobbyCircle      from '@/assets/circles/hobby_circle.png'
import kidsCircle       from '@/assets/circles/kids_circle.png'
import scienceCircle    from '@/assets/circles/science_circle.png'

const router = useRouter()
const wrapper = ref(null)
const userStore = useUserStore()
const isLoggedIn = computed(() => userStore.isLoggedIn)

function scrollTo(id) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })
}
function logout() {
  userStore.logout()
  router.push('/')
}

// 테마 배열
const themes = [
  { id: 1, label: '소설/시/희곡', icon: iconNovel },
  { id: 2, label: '경제/경영',     icon: iconBusiness },
  { id: 3, label: '자기계발',       icon: iconSelf },
  { id: 4, label: '인문/교양',       icon: iconHumanities },
  { id: 5, label: '취미/실용',       icon: iconHobby },
  { id: 6, label: '어린이/청소년',   icon: iconKids },
  { id: 7, label: '과학',           icon: iconScience },
]

// 인기 감상평 더미
const popularReviews = [
  {
    id: 1,
    img: novelCircle,
    title: '마음에 남는 이야기',
    text: '섬세한 문장과 깊은 여운이 어우러진 작품입니다.',
  },
  {
    id: 2,
    img: selfCircle,
    title: '놀라운 일상',
    text: '작지만 강한 변화가 필요할 때 추천하고 싶어요.',
  },
  {
    id: 3,
    img: kidsCircle,
    title: '따뜻한 이야기',
    text: '어린이도 공감할 수 있고, 어른도 돌아보게 만드는 이야기예요.',
  },
]

// 인기 열린결말 더미
const popularEndings = [
  {
    id: 1,
    img: businessCircle,
    title: '어느 봄날의 약속',
    text: '만남 이후 펼쳐질 이야기를 상상하게 하는 열린 결말.',
  },
  {
    id: 2,
    img: humanitiesCircle,
    title: '당신의 선택은 계속된다',
    text: '마지막 문장이 큰 울림을 주는 작품입니다.',
  },
  {
    id: 3,
    img: scienceCircle,
    title: '시간이 멈춘 학교',
    text: '판타지와 현실을 넘나드는 흥미로운 결말.',
  },
]
</script>

<style scoped>
.home-page {
  position: relative;
  height: 100vh;
  overflow: hidden;
}

/* 스크롤 스냅 */
.sections-wrapper {
  height: 100%;
  overflow-y: auto;
  scroll-snap-type: y mandatory;
}
.section {
  position: relative;
  height: 100vh;
  scroll-snap-align: start;
  padding-top: 4rem;
}
.section:not(#section3) {
  height: 100vh;
}

/* Hero */
.hero {
  background: #ffc93c;
  display: flex;
  align-items: center;
  justify-content: center;
}
.hero-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1920px;
  margin: 0 auto;
  padding: 0 10%;
}
.hero-text { flex-basis: 45%; }
.hero-text h1 { font-size: 2.5rem; margin-bottom: 1rem; color: #000; }
.hero-text p { line-height: 1.6; margin-bottom: 2rem; color: #333; }
.hero-image { width: clamp(400px,30vw,600px); height: auto; }
.btn-primary {
  padding: .75rem 1.5rem;
  background: #000;
  color: #fff;
  border-radius: 8px;
  border: none;
  cursor: pointer;
}

.scroll-arrow {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  font-size: 2rem;
  cursor: pointer;
  animation: pulse 1s infinite alternate;
}
@keyframes pulse { to { transform: translateX(-50%) scale(1.2); } }
.scroll-arrow:hover { animation-play-state: paused; }

/* 섹션2 */
.theme-best { padding: 2rem; }
.theme-grid {
  display: flex;
  justify-content: space-around;
  background: #fff4c8;
  padding: 2rem 0;
}
.theme-item {
  width: 120px; height: 120px;
  background: #fff; border-radius: 1rem;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  box-shadow: 0 0 6px rgba(0,0,0,0.1);
  cursor: pointer;
}
.theme-item img { width: 50px; height: 50px; margin-bottom: .5rem; }
.best-seller .books {
  display: flex; justify-content: space-between;
}
.book-card {
  width: 22%; padding: 1rem;
  background: #fff;
  box-shadow: 0 0 6px rgba(0,0,0,0.1);
}

/* 섹션3 */

.popular {
  background: #fff;
  padding: 2rem 10%;
}
.popular-block {
  position: relative;
  margin-top: 5rem;
}
.popular-content {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}
.popular-info {
  width: 25%;
}
.overlay-text {
  position: absolute;
  top: -50px;
  left: 0;
  font-size: 6rem;
  font-weight: bold;
  /* 채우기는 완전히 투명 */
  color: transparent;
  /* WebKit 계열 (Chrome, Safari) */
  -webkit-text-stroke-width: 0.5px;
  -webkit-text-stroke-color: rgb(255, 153, 0);
  z-index: 0;
}
.heading {
  font-size: 3rem;
  margin-bottom: .5rem;
}
.subheading {
  color: #666;
  font-size: .95rem;
  margin-bottom: 1.5rem;
}
.dots {
  display: flex;
  margin-top: 1rem;
}
.dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: #ddd;
  margin-right: 8px;
}
.dot.active {
  background: #333;
}

.popular-cards {
  width: 70%;
  display: flex;
  justify-content: space-between;
  gap: 2rem;
}
.card {
  flex: 2;
  background: #fff;
  padding: 2rem;
  border-radius: 3rem;
  box-shadow: 0 0 6px rgba(0,0,0,0.1);
  text-align: left;
  width: 150px;
  height: 400px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.card:hover {
  /* 살짝 확대 */
  transform: scale(1.05);
  /* 강조를 위해 그림자도 조금 강하게 */
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.card-badge {
  display: block;
  width: 50px; height: 50px;
  object-fit: cover;
  margin-bottom: 1rem;
}
.quote {
  font-size: 1.25rem;
  margin-bottom: .5rem;
}
.text {
  color: #333;
  line-height: 1.4;
}
.heading,
.subheading,
.card {
  position: relative;
  z-index: 1;
}
.popular-block .heading {
  position: relative;
  /* 텍스트 왼쪽에 여유를 줘야 네모가 겹치지 않아요 */
  padding-left: 0.5rem;
}

/* 2) ::before 로 네모 만들기 */
.popular-block .heading::before {
  content: "";
  position: absolute;
  top: 0.5rem;    /* 텍스트 라인보다 살짝 위로 */
  left: 0rem;          /* padding-left 만큼 밀어넣어짐 */
  width: 1.8rem;   /* 네모 크기 */
  height: 1.8rem;  /* 네모 크기 */
  background: rgb(255, 153, 0);
  /* 모서리를 살짝 둥글리고 싶으면 아래 주석 해제 */
  z-index: -1;
}
</style>
