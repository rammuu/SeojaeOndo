# accounts/urls.py
from django.urls import path
from .views import CustomRegisterView
from .views import  NaverLogin, KakaoLogin, CustomGoogleLoginView

urlpatterns = [
    path('registration/', CustomRegisterView.as_view(), name='custom_register'),
    path('google/', CustomGoogleLoginView.as_view(), name='google_login'),
    path("naver/", NaverLogin.as_view(), name="naver_login"),
    path("kakao/", KakaoLogin.as_view(), name="kakao_login"),
]
