from django.urls import path
from .views import *

app_name="blog_app"

urlpatterns = [
    path('posts/', BlogListView.as_view(), name="posts"),
    path('my_posts/', MyPostsListView.as_view(), name="my_posts"),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug_id>', BlogDetailView.as_view(),name="post"),
    path('post/<int:pk>', BlogDetailView.as_view(),name="post_by_pk"),
    path('delete_post/<int:pk>', BlogDeleteView.as_view(),name="delete_post"),
    path('update_post/<int:pk>',BlogUpdateView.as_view() ,name="update_post"),
    path('create_post/', BlogPostCreateView.as_view() ,name="create_post"),
]
