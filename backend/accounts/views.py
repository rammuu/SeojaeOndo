# accounts/views.py
from dj_rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer # Keep CustomRegisterSerializer if used by CustomRegisterView
# Removed SocialApp, provider-specific adapters, SocialLoginView, OAuth2Client as custom social views are removed
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from .serializers import UserSerializer
from books.serializers import BookSerializer
from rest_framework.authtoken.models import Token # Keep if token generation is needed elsewhere, or remove if adapter handles all
from rest_framework import status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

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

@method_decorator(csrf_exempt, name='dispatch')
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class FollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_pk):
        try:
            user_to_follow = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user == user_to_follow:
            return Response({'error': 'You cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        # Using the through model 'Follow' to create the relationship
        # from_user is request.user, to_user is user_to_follow
        from .models import Follow # Import Follow model
        follow_instance, created = Follow.objects.get_or_create(
            from_user=request.user, 
            to_user=user_to_follow
        )

        if created:
            return Response({'status': 'followed'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'already following'}, status=status.HTTP_200_OK)

    def delete(self, request, user_pk):
        try:
            user_to_unfollow = User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        from .models import Follow # Import Follow model
        deleted_count, _ = Follow.objects.filter(
            from_user=request.user,
            to_user=user_to_unfollow
        ).delete()

        if deleted_count > 0:
            return Response({'status': 'unfollowed'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'not following'}, status=status.HTTP_404_NOT_FOUND)


class MyBookshelfView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books = request.user.bookshelf.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({'message': '회원 탈퇴가 완료되었습니다.'}, status=status.HTTP_204_NO_CONTENT)