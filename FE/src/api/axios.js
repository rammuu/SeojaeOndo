import axios from 'axios';
import { useUserStore } from '@/stores/user'; // Pinia 스토어 임포트

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',  // Django API 주소
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터 추가
api.interceptors.request.use(
  (config) => {
    // Pinia 스토어는 컴포넌트 외부에서 직접 접근하기 어려우므로,
    // 일반적으로 로컬 스토리지에서 토큰을 가져옵니다.
    // user.js 스토어의 logout 액션에서 localStorage.removeItem('authToken')을 사용하므로,
    // 로그인 시 'authToken' 키로 토큰이 저장된다고 가정합니다.
    const token = localStorage.getItem('authToken'); 
    
    // Pinia 스토어가 초기화된 후 토큰을 가져오려면, 스토어 인스턴스를 사용해야 합니다.
    // 하지만 인터셉터는 스토어 인스턴스 생성 전에 실행될 수 있으므로,
    // localStorage를 우선적으로 확인하거나, main.js 등에서 스토어 초기화 후 
    // api.defaults.headers.common['Authorization']을 설정하는 방법도 고려할 수 있습니다.
    // 여기서는 localStorage를 사용하는 간단한 방식을 택합니다.
    // 더 복잡한 상태 관리가 필요하면 main.js에서 처리하는 것이 좋습니다.

    if (token) {
      // Django REST Framework의 기본 TokenAuthentication은 'Token <token_value>' 형식을 사용합니다.
      config.headers['Authorization'] = `Token ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
