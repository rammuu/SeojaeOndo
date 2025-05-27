from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register(r'categories', CategoryViewSet, basename='category')
# router.register(r'books', BookViewSet, basename='book')
# router.register(r'threads', ThreadViewSet, basename='thread') # ThreadViewSet 등록

urlpatterns = [
    # path('', include(router.urls)),

    path("<int:book_pk>/", views.BookDetailAPIView.as_view(), name="detail"),
    path("<int:book_pk>/threads/", views.ThreadListAPIView.as_view(), name="thread_list"), # 감상평 목록 URL 추가
    path("<int:book_pk>/recommendations/", views.BookRecommendationAPIView.as_view(), name="book_recommendations"), # 책 추천 API URL 추가
    
    path("<int:book_pk>/thread/create/", views.ThreadCreateAPIView.as_view(), name="thread_create"),
    path("<int:book_pk>/thread/<int:thread_pk>/", views.ThreadDetailAPIView.as_view(), name="thread_detail"),
    path("<int:book_pk>/thread/<int:thread_pk>/update/", views.ThreadUpdateAPIView.as_view(), name="thread_update"),
    path("<int:book_pk>/thread/<int:thread_pk>/delete/", views.ThreadDeleteAPIView.as_view(), name="thread_delete"),
    path("<int:book_pk>/thread/<int:thread_pk>/likes/", views.ThreadLikeAPIView.as_view(), name="likes"),
    
    path("<int:thread_pk>/comment/create/", views.CommentCreateAPIView.as_view(), name="create_comment"),
    path("<int:thread_pk>/comment/<int:comment_pk>/delete/", views.CommentDeleteAPIView.as_view(), name="delete_comment"),
    path('comment/<int:comment_pk>/like/', views.CommentLikeAPIView.as_view(), name='comment_like'),
    path("<int:thread_pk>/comment/", views.ThreadCommentListAPIView.as_view(), name="thread_comment_list"),
    path("<int:thread_pk>/comment/<int:comment_pk>/update/", views.CommentUpdateAPIView.as_view(), name="update_comment"),

    path("", views.FilterCategoryAPIView.as_view(), name="filter_category"),
    path('search/', views.FilterBookAPIView.as_view(), name='book-filter'),
    path('<int:book_id>/bookshelf/', views.ToggleBookshelfView.as_view()),

    path('alternate-ending/', views.AlternateEndingView.as_view(), name='alternate-ending'),
    path('<int:book_pk>/open-endings/', views.OpenEndingCreateView.as_view(), name='open-ending-create'),
    path('<int:book_id>/endingslist/', views.BookOpenEndingsView.as_view(), name='book-open-endings'),
    path('open-endings/<int:pk>/', views.OpenEndingDetailView.as_view(), name='open-ending-detail'),

    path('open-endings/<int:pk>/like/', views.OpenEndingLikeToggleView.as_view(), name='open-ending-like'),
    path('open-endings/<int:pk>/comments/', views.OpenEndingCommentView.as_view(), name='open-ending-comments'),
    path('open-endings/comments/<int:comment_id>/', views.OpenEndingCommentDetailView.as_view(), name='open-ending-comment-detail'),
]
