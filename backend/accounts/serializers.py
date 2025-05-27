from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'nickname', 'phone_number', 'favorite_categories']


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
    

class FollowingUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'name']

class FollowerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'name']