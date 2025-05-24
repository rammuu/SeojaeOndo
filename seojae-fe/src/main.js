// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'   // ✅ 라우터 가져오기


const app = createApp(App)

app.use(router)                 // ✅ 라우터 연결
app.mount('#app')
