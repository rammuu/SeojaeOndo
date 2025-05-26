# accounts/urls.py
from django.urls import path
from .views import  CustomRegisterView, check_nickname, check_username, UserInfoView, FollowView

urlpatterns = [
    path('registration/', CustomRegisterView.as_view(), name='custom_register'),
    path('check-username/', check_username),
    path('check-nickname/', check_nickname),
    path('user/', UserInfoView.as_view(), name='user-info'),
    path('users/<int:user_pk>/follow/', FollowView.as_view(), name='user-follow'),
]
