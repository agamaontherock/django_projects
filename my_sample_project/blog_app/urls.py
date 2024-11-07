from .views import *
from django.urls import path

app_name = "blog_app"
urlpatterns = [
    path('posts/', BlogListView.as_view(), name = 'posts'),
    path('post/<int:pk>', BlogDetailView.as_view(), name='post'),
    path('delete_post/<int:pk>', BlogDeleteView.as_view(), name='delete_post'),
    path('update_post/<int:pk>', BlogUpdateView.as_view(), name='update_post'),
    path('create_post/', BlogPostCreateView.as_view(), name="create_post")
]