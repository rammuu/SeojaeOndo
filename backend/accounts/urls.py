# accounts/urls.py
from django.urls import path
from .views import  CustomRegisterView, NaverLogin, KakaoLogin, CustomGoogleLoginView, check_nickname, check_username

urlpatterns = [
    path('registration/', CustomRegisterView.as_view(), name='custom_register'),
    path('google/', CustomGoogleLoginView.as_view(), name='google_login'),
    path("naver/", NaverLogin.as_view(), name="naver_login"),
    path("kakao/", KakaoLogin.as_view(), name="kakao_login"),
    path('check-username/', check_username),
    path('check-nickname/', check_nickname),
]
