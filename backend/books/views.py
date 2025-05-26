from django.shortcuts import get_object_or_404 # 추가
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions # generics, permissions 추가
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book, Thread, Comment # Category 모델은 현재 뷰에서 사용하지 않으므로 그대로 둡니다.
from .serializers import (
    BookSerializer, ThreadSerializer, CommentSerializer # CategorySerializer도 그대로 둡니다.
)
from .utils import generate_image_with_openai
from .recommender import recommend_books
# IsOwnerOrReadOnly 와 utils는 ThreadListAPIView에서 직접 사용하지 않으므로 일단 그대로 둡니다.


class BookListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, book_pk):
        try:
            book = Book.objects.get(pk=book_pk)
            # recommendations = recommend_books(book.title, top_n = 6)
            book_data = BookSerializer(book).data
            # book_data['recommendations'] = [BookSerializer(b).data for b in recommendations]
            return Response(book_data)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)


class ThreadCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_pk):
        try:
            book = Book.objects.get(pk=book_pk)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ThreadSerializer(data=request.data, context={"request": request, "book": book})
        if serializer.is_valid():
            thread = serializer.save()
            generated_image_path = generate_image_with_openai(thread.title, thread.content, book.title, book.author)
            if generated_image_path:
                thread.cover_img = generated_image_path
                thread.save()
            return Response(ThreadSerializer(thread).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThreadDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, book_pk, thread_pk):
        try:
            thread = Thread.objects.get(pk=thread_pk, book_id=book_pk)
            serializer = ThreadSerializer(thread)
            return Response(serializer.data)
        except Thread.DoesNotExist:
            return Response({"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND)


class ThreadUpdateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def patch(self, request, book_pk, thread_pk):
        try:
            thread = Thread.objects.get(pk=thread_pk, book_id=book_pk)
        except Thread.DoesNotExist:
            return Response({"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND)

        if thread.user != request.user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = ThreadSerializer(thread, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ThreadDeleteAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, book_pk, thread_pk):
        try:
            thread = Thread.objects.get(pk=thread_pk, book_id=book_pk)
        except Thread.DoesNotExist:
            return Response({"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND)

        if thread.user != request.user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ThreadLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_pk, thread_pk):
        try:
            thread = Thread.objects.get(pk=thread_pk, book_id=book_pk)
        except Thread.DoesNotExist:
            return Response({"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user in thread.likes.all():
            thread.likes.remove(user)
            liked = False
        else:
            thread.likes.add(user)
            liked = True

        return Response({
            'liked': liked,
            'like_count': thread.likes.count()
        })

class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, thread_pk):
        try:
            # book = Book.objects.get(pk=book_pk)
            thread = Thread.objects.get(pk=thread_pk)
        except (Thread.DoesNotExist):
            return Response({"error": "Invalid book or thread"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(thread=thread, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDeleteAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def delete(self, request, thread_pk, comment_pk):
        try:
            comment = Comment.objects.get(pk=comment_pk, thread_id=thread_pk)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FilterCategoryAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        category = request.query_params.get("category")
        if category:
            books = Book.objects.filter(category=category)
        else:
            books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class FilterBookAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        search = request.query_params.get("search")

        books = Book.objects.all()

        if search:
            books = books.filter(title__icontains=search)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class ThreadListAPIView(generics.ListAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # 또는 IsAuthenticated

    def get_queryset(self):
        book_pk = self.kwargs.get('book_pk')
        book = get_object_or_404(Book, pk=book_pk)
        # 해당 책(book)에 연결된 Thread 객체들만 필터링하고, 최신순으로 정렬합니다.
        return Thread.objects.filter(book=book).order_by('-created_at')

    # Serializer context에 request를 전달하여 SerializerMethodField에서 사용할 수 있도록 합니다.
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class ThreadCommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, thread_pk):
        try:
            thread = Thread.objects.get(pk=thread_pk)
        except Thread.DoesNotExist:
            return Response({"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(thread=thread).order_by('created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BookRecommendationAPIView(APIView):
    permission_classes = [permissions.AllowAny] # 추천은 누구나 볼 수 있도록 (필요시 IsAuthenticated 등으로 변경)

    def get(self, request, book_pk):
        from .recommender import recommend_books

        try:
            # 기준 책이 존재하는지 먼저 확인 (선택 사항, recommend_books 내부에서도 처리함)
            base_book = get_object_or_404(Book, pk=book_pk)
        except Book.DoesNotExist: # get_object_or_404가 Http404를 발생시키므로 사실 이 블록은 실행 안됨
            return Response({"error": "기준이 되는 책을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 추천 책 목록 가져오기 (top_n은 기본값 또는 쿼리 파라미터로 받을 수 있음)
        top_n_param = request.query_params.get('top_n', 3)
        try:
            top_n = int(top_n_param)
        except ValueError:
            top_n = 3

        try:
            base_book = Book.objects.get(pk=book_pk)
        except Book.DoesNotExist:
            return Response({"error": "기준이 되는 책을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        recommended_books_list = recommend_books(base_book.title, request.user, top_n=top_n, base_book_id=book_pk)

        if not recommended_books_list:
            return Response({"message": "추천할 책이 없거나 추천 과정에서 오류가 발생했습니다."}, status=status.HTTP_200_OK)

        # BookSerializer를 사용하여 추천된 책 목록 직렬화
        # context에 request를 전달하여 이미지 URL 등이 절대 경로로 생성되도록 함
        serializer = BookSerializer(recommended_books_list, many=True, context={'request': request})
        data = serializer.data
        print(f"추천된 책 목록: {data}")
        return Response(data, status=status.HTTP_200_OK)



class CommentLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_pk):
        try:
            comment = Comment.objects.get(pk=comment_pk)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if user in comment.likes.all():
            comment.likes.remove(user)
            liked = False
        else:
            comment.likes.add(user)
            liked = True

        return Response({
            "liked": liked,
            "like_count": comment.likes.count()
        }, status=status.HTTP_200_OK)


class CommentUpdateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def patch(self, request, thread_pk, comment_pk):
        try:
            comment = Comment.objects.get(pk=comment_pk, thread_id=thread_pk)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ToggleBookshelfView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "책을 찾을 수 없습니다."}, status=404)

        user = request.user
        if book in user.bookshelf.all():
            user.bookshelf.remove(book)
            return Response({"message": "서재에서 제거되었습니다.", "in_bookshelf": False})
        else:
            user.bookshelf.add(book)
            return Response({"message": "서재에 추가되었습니다.", "in_bookshelf": True})