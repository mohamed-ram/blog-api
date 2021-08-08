from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # post api
    
    # path('posts/', views.PostListAPIView.as_view()),
    
    # custom search
    # path('posts/', views.PostListWithSearchAPIView.as_view()),
    
    # built in search and filter
    # path('posts/', views.PostListWithRESTSearchAPIView.as_view()),
    # pagination.
    # path('posts/', views.PostListWithPaginationAPIView.as_view()),
    
    # post api with comments in hyperlink..
    path('posts/', views.PostListAPIViewWithHyperlinkComments.as_view()),
    
    
    path('posts/create/', views.PostCreateAPIView.as_view()),
    path('posts/update/<pk>/', views.PostUpdateAPIView.as_view()),
    path('posts/delete/<pk>/', views.PostDeleteAPIView.as_view()),
    path('posts/<str:slug>/', views.PostDetailAPIView.as_view()),
    
    # category api
    path('categories/', views.CategoryListAPIView.as_view()),
    path('category/create/', views.CategoryCreateAPIView.as_view()),
    path('category/update/<pk>/', views.CategoryUpdateAPIView.as_view()),
    path('category/delete/<pk>/', views.CategoryDeleteAPIView.as_view()),
    path('category/<pk>/', views.CategoryDetailAPIView.as_view()),
    
    # comments api
    path('posts/<post_pk>/comments/', views.CommentListAPIView.as_view(), name='post-comments'),
    path('posts/<post_pk>/comments/create/', views.CommentCreateAPIView.as_view()),
    path('posts/<post_pk>/comments/update/<pk>/', views.CommentUpdateAPIView.as_view()),
    path('posts/<post_pk>/comments/delete/<pk>/', views.CommentDeleteAPIView.as_view()),
    path('posts/<post_pk>/comments/<pk>/', views.CommentDetailAPIView.as_view()),
]

