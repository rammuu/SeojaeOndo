from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.helpers import complete_social_login
from django.contrib.auth import get_user_model
from rest_framework import serializers
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.models import SocialToken
import requests


User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    nickname = serializers.CharField(required=True)
    favorite_categories = serializers.ListField(child=serializers.CharField(), required=True)

    def save(self, request):
        user = super().save(request)
        user.email = self.validated_data['email']
        user.name = self.validated_data['name']
        user.phone_number = self.validated_data['phone_number']
        user.nickname = self.validated_data['nickname']
        user.favorite_categories = self.validated_data['favorite_categories']
        user.save()
        return user


def get_user_social_token(user):
    try:
        token = SocialToken.objects.get(account__user=user, account__provider='google')
        return token
    except SocialToken.DoesNotExist:
        return None
    

class GoogleSocialLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    nickname = serializers.CharField(required=True)
    favorite_categories = serializers.ListField(child=serializers.CharField(), required=False)

    def validate(self, attrs):
        request = self.context.get('request')
        access_token = attrs.get('access_token')

        adapter = GoogleOAuth2Adapter(request)
        app = SocialApp.objects.get(provider='google')
        token = SocialToken(token=access_token, app=app)

        # ✅ 구글 사용자 정보 가져오기 (response 대체)
        user_info_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(user_info_url, headers=headers)

        if not response.ok:
            raise serializers.ValidationError({'access_token': 'Failed to fetch user info from Google'})

        login = adapter.complete_login(request, app, token, response.json())
        login.token = token

        try:
            complete_social_login(request, login)
        except OAuth2Error as e:
            raise serializers.ValidationError({'access_token': 'Google login failed. ' + str(e)})

        user = login.user

        google_email = response.json().get("email")
        if google_email:
            user.email = google_email

        user.name = attrs.get('name')
        user.phone_number = attrs.get('phone_number')
        user.nickname = attrs.get('nickname')
        user.favorite_categories = attrs.get('favorite_categories', [])
        user.save()

        attrs['user'] = user
        return attrs