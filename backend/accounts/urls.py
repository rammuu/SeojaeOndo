# accounts/urls.py
from django.urls import path
from .views import FollowerListView, FollowingListView, DeleteAccountView, MyBookshelfView, CustomRegisterView, check_nickname, check_username, UserInfoView, FollowView

urlpatterns = [
    path('signup/', CustomRegisterView.as_view(), name='custom_register'),
    path('check-username/', check_username),
    path('check-nickname/', check_nickname),
    path('userinfo/', UserInfoView.as_view(), name='user-info'),
    path('<int:user_pk>/follow/', FollowView.as_view(), name='user-follow'),
    path('following/', FollowingListView.as_view(), name='following-list'),
    path('followers/', FollowerListView.as_view(), name='follower-list'),
    path('delete/', DeleteAccountView.as_view(), name='delete-account'),
    path('bookshelf/', MyBookshelfView.as_view()),
]
