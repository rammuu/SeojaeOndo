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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.shortcuts import redirect
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialLogin, SocialAccount
import requests
from rest_framework.authtoken.models import Token
from asgiref.sync import async_to_sync

from allauth.account.utils import perform_login

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
def check_username(request):
    username = request.query_params.get('username')
    if not username:
        return Response({'error': 'username parameter required'}, status=400)

    exists = User.objects.filter(username=username).exists()
    return Response({'available': not exists})

@api_view(['GET'])
@permission_classes([AllowAny])
def check_nickname(request):
    nickname = request.query_params.get('nickname')
    if not nickname:
        return Response({'error': 'nickname parameter required'}, status=400)

    exists = User.objects.filter(nickname=nickname).exists()
    return Response({'available': not exists})

class CustomGoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/accounts/google/login/callback/"
    client_class = OAuth2Client
    serializer_class = GoogleSocialLoginSerializer

class NaverLogin(SocialLoginView):
    adapter_class = NaverOAuth2Adapter
    callback_url = "http://localhost:5173/naver/callback"
    client_class = OAuth2Client
    serializer_class = GoogleSocialLoginSerializer

    def post(self, request, *args, **kwargs):
        print("🔥 POST 요청 도착")
        print("🔥 request.data =", request.data)
        return super().post(request, *args, **kwargs)


class NaverLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("🔥 네이버 로그인 POST 도착")
        print("🔥 request.data =", request.data)
        code = request.data.get('code')
        state = request.data.get('state')

        try:
            app = SocialApp.objects.get(provider='naver')
        except SocialApp.DoesNotExist:
            return Response({'error': 'Naver SocialApp 설정이 필요합니다.'}, status=500)

        token_url = 'https://nid.naver.com/oauth2.0/token'
        token_params = {
            'grant_type': 'authorization_code',
            'client_id': app.client_id,
            'client_secret': app.secret,
            'code': code,
            'state': state,
        }
        token_response = requests.get(token_url, params=token_params)
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        print("🧾 token_data =", token_data)

        if not access_token:
            return Response({'error': '네이버 access_token 요청 실패'}, status=400)

        userinfo_url = 'https://openapi.naver.com/v1/nid/me'
        userinfo_response = requests.get(userinfo_url, headers={
            'Authorization': f'Bearer {access_token}'
        })
        userinfo = userinfo_response.json()

        print("🧾 userinfo =", userinfo)
        if userinfo.get('resultcode') != '00':
            return Response({'error': '네이버 사용자 정보 요청 실패'}, status=400)

        adapter = NaverOAuth2Adapter(request)
        token_dict = {'access_token': access_token}

       
        response_data = userinfo['response']
        uid = response_data['id']
        name = response_data.get('name', '')
        nickname = response_data.get('nickname', '')
        phone = response_data.get('mobile', '')
        email = f"{uid}@naver.com"  # 네이버는 기본 이메일 제공 안하므로 대체 이메일 구성

        # 유저가 이미 존재하는지 확인 또는 새로 생성
        user, created = User.objects.get_or_create(username=uid, defaults={
            'email': email,
            'name': name,
            'nickname': nickname,
            'phone_number': phone,
        })

        # 소셜 계정 객체 구성
        sociallogin = SocialLogin(
            user=user,
            account=SocialAccount(
                user=user,
                uid=uid,
                provider='naver',
                extra_data=response_data
            )
        )

        # 로그인 처리
        if created:
            print("🆕 새 사용자 → complete_social_login 실행")
            complete_social_login(request, sociallogin)
        else:
            print("👤 기존 사용자 → perform_login 실행")
            perform_login(request, user, email_verification='optional')

        # Django 토큰 발급 및 프론트 리디렉션
        token_obj, _ = Token.objects.get_or_create(user=user)
        redirect_url = f"http://localhost:5173/social-login/callback/?token={token_obj.key}"
        print("🔁 리디렉션 URL:", redirect_url)
        return Response({'token': token_obj.key}, status=200)

class KakaoLogin(SocialLoginView):
    adapter_class = KakaoOAuth2Adapter
    serializer_class = GoogleSocialLoginSerializer

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.GET, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)