from django.contrib import admin
from .models import Post, Category, Comment, Replay, Like

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Replay)
admin.site.register(Like)


class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'slug', 'category', 'timestamp']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin)

