# accounts/views.py
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.naver.views import NaverOAuth2Adapter
from allauth.socialaccount.providers.kakao.views import KakaoOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from .serializers import GoogleSocialLoginSerializer
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

class CustomGoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/accounts/google/login/callback/"
    client_class = OAuth2Client
    serializer_class = GoogleSocialLoginSerializer

class NaverLogin(SocialLoginView):
    adapter_class = NaverOAuth2Adapter
    serializer_class = GoogleSocialLoginSerializer

class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    serializer_class = GoogleSocialLoginSerializer

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
