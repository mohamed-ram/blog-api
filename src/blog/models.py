from django.contrib.auth.models import User
from django.db import models


def upload(instance, img_name):
    return f"posts/{instance.author}/{img_name}"


# Post model
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, blank=False)
    content = models.TextField(max_length=1000, blank=True)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to=upload, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title


# Category model
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.title


# Comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content


# Replay model
class Replay(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replays')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content


# Like model
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user} likes {self.post}'
