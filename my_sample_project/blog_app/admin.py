from django.contrib import admin
from .models import BlogPost, Comment
# Register your models here.
# admin.site.register(BlogPost)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "owner", "status", "published_at"]
    list_filter = ["owner", "status"]
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["user", "blogpost", "active"]
    list_filter = ["user", "active"]