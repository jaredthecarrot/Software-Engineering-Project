from django.contrib import admin
from .models import Post, LikePost, PostComment

# Register your models here.
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(PostComment)

