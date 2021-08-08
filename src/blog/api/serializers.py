from django.contrib.auth.models import User
from rest_framework import serializers
from ..models import Category, Comment, Like, Post, Replay


# user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_superuser']
        read_only_fields = ['first_name', 'last_name', 'is_superuser']


# Category serializer.
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']
        read_only_fields = ['slug']


# Replays serializer.
class ReplaySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Replay
        fields = ['id', 'user', 'content', 'timestamp']
        read_only_fields = ['comment']


# Comment serializer.
class CommentSerializer(serializers.ModelSerializer):
    replays = ReplaySerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    replays_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'timestamp', 'replays_count', 'replays']
        read_only_fields = ['post', 'user']
    
    def get_replays_count(self, obj):
        replays = Replay.objects.filter(comment=obj)
        return replays.count()

# like serializer
class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Like
        fields = ['user']
        read_only_fields = ['user', 'post']


# Post serializer.
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ["id", "title", "content", "slug", "image", "timestamp",
                  "updated", "published", "likes", "author", "category", 'comments']
        read_only_fields = ['author', 'slug']


# Post serializer with hyperlink comment serializer.
class PostSerializerWithHyperlinkComments(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    comments = serializers.HyperlinkedIdentityField(view_name='api:post-comments', read_only=True,
                                                    lookup_url_kwarg='post_pk')
    
    
    class Meta:
        model = Post
        fields = ["id", "title", "content", "slug", "image", "timestamp",
                  "updated", "published", "likes", "author", "category", 'comments']
        read_only_fields = ['author', 'slug']


