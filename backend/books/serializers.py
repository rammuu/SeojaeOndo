# serializers.py
from rest_framework import serializers
from .models import Book, Thread, Comment, Category, OpenEnding, OpenEndingLike, OpenEndingComment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'isbn', 'cover', 'publisher',
            'pub_date', 'author', 'author_info', 'author_photo',
            'customer_review_rank', 'subTitle', 'category'
        ]



class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = ['id', 'title', 'content', 'cover_img', 'book', 'user']
        read_only_fields = ['id', 'cover_img', 'book', 'user']

    def create(self, validated_data):
        # context에서 book, user를 가져와서 주입
        book = self.context.get('book')
        user = self.context['request'].user
        title = validated_data.get('title', '')
        content = validated_data.get('content', '')

        return Thread.objects.create(title=title, content=content, book=book, user=user)

class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'thread', 'user', 'created_at', 'like_count']
        read_only_fields = ['id', 'thread', 'user', 'created_at', 'like_count']

    def get_like_count(self, obj):
        return obj.likes.count()
    


class OpenEndingSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = OpenEnding
        fields = ['id', 'user_nickname', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

class OpenEndingCommentSerializer(serializers.ModelSerializer):
    user_nickname = serializers.CharField(source='user.nickname', read_only=True)

    class Meta:
        model = OpenEndingComment
        fields = ['id', 'user_nickname', 'content', 'created_at']

class OpenEndingLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenEndingLike
        fields = ['id', 'user', 'open_ending', 'created_at']
        read_only_fields = ['id', 'created_at']