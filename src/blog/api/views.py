from django.db.models import Q
from django.utils.text import slugify
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView, \
    DestroyAPIView

from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .permissions import IsCommentOwner
from .serializers import CategorySerializer, CommentSerializer, LikeSerializer, \
    PostSerializer, PostSerializerWithHyperlinkComments
from ..models import Category, Comment, Like, Post

#######################################
####### Post API Views ################
#######################################


# Post List api view without filter..
class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# post list api view with hyperlink comments.
class PostListAPIViewWithHyperlinkComments(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerWithHyperlinkComments
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    


# filtering Post List api view by overriding queryset.
class PostListWithSearchAPIView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self, *args, **kwargs):
        # queryset = super(FilterPostListAPIView, self).get_queryset(*args, **kwargs)
        posts = Post.objects.all()
        query = self.request.GET.get('search')
        if query and query != "":
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__username__icontains=query)
            ).distinct()
        return posts


# filtering Post List api view by adding filter_backends.
class PostListWithRESTSearchAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'author__username']


# filtering Post List api view by overriding queryset.
class PostListWithPaginationAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # search
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content', 'author__username']
    # pagination
    # we can assign them to settings.py file as default or create custom ones.
    # pagination_class = PostLimitOffsetPagination
    pagination_class = PostPageNumberPagination


# get specific post
class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    # lookup_url_kwarg = 'pk'


# create new post
class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # we need to access user, slug before saving.
    def perform_create(self, serializer):
        # print(serializer.data)
        # print('initial data', serializer.initial_data)
        # print('validated data', serializer.validated_data)
        
        author = self.request.user
        slug = slugify(serializer.validated_data.get('title'))
        serializer.save(author=author, slug=slug)


# update post api
# or we can use UpdateRetrieveAPIView to get old/exist data in the form.
class PostUpdateAPIView(UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
        
    def perform_update(self, serializer):
        print('initial data: ', serializer.initial_data)
        print('validated data: ', serializer.validated_data)
        slug = slugify(serializer.validated_data.get('title'))
        author = self.request.user
        serializer.save(author=author, slug=slug)


# delete post api
class PostDeleteAPIView(DestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)



#######################################
####### Category API Views ################
#######################################


# Category List api view.
class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# get specific category
class CategoryDetailAPIView(RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # lookup_field = 'slug'
    lookup_url_kwarg = 'pk'


# create new post
class CategoryCreateAPIView(CreateAPIView):
    # queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    
    def perform_create(self, serializer):
        slug = slugify(serializer.validated_data.get('title'))
        serializer.save(slug=slug)
        
    
# update post api
class CategoryUpdateAPIView(UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    
    def perform_update(self, serializer):
        slug = slugify(serializer.validated_data.get('title'))
        serializer.save(slug=slug)


# delete post api
class CategoryDeleteAPIView(DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    
    def perform_destroy(self, instance):
        print(f'{instance.title} have deleted successfully')
        return super(CategoryDeleteAPIView, self).perform_destroy(instance)
    

#######################################
####### Comment API Views #############
#######################################


# Comment List api view.
class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        return Comment.objects.filter(post=post)


# get specific Comment
class CommentDetailAPIView(RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # lookup_field = 'slug'
    lookup_url_kwarg = 'pk'
    
    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        return Comment.objects.filter(post=post)


# create new Comment
class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Post.objects.get(pk=self.kwargs['post_pk'])
        
    def perform_create(self, serializer):
        user = self.request.user
        post = self.get_queryset()
        serializer.save(post=post, user=user)


# update Comment api
class CommentUpdateAPIView(UpdateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentOwner]
    
    def get_queryset(self):
        # return Comment.objects.filter(pk=self.kwargs['pk'], user=self.request.user)
        return Comment.objects.filter(pk=self.kwargs['pk'])

    def perform_create(self, serializer):
        user = self.request.user
        post = Post.objects.filter(pk=self.kwargs['post_pk'])
        serializer.save(post=post, user=user)


# delete post api
class CommentDeleteAPIView(DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        return Comment.objects.filter(pk=self.kwargs['pk'], user=self.request.user)
    
    def perform_destroy(self, instance):
        print(f'\'{instance.content}\' successfully deleted!')
        return super(CommentDeleteAPIView, self).perform_destroy(instance)



#######################################
####### Toggle Post Like ##############
#######################################

class ToggleLikeAPIView(UpdateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
