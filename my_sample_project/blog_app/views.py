from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import BlogPost
from django.http import Http404
from .ownerviews import *
from django.utils import timezone

class BlogListView(ListView):
    model = BlogPost
    paginate_by = 5
    queryset = BlogPost.objects.all()
    
class MyPostsListView(ListView):
    model = BlogPost
    paginate_by = 5
    queryset = BlogPost.published_objects.all()

class BlogDetailView(DetailView):
    model = BlogPost
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        slug_id = self.kwargs.get("slug_id")

        if pk:
            return get_object_or_404(self.model, pk=pk)
        elif slug_id:
            return get_object_or_404(self.model, created_at__year=year, created_at__month=month, created_at__day=day, slug = slug_id)
        else:
            raise Http404("No object found matching the provided criteria.")

class BlogDeleteView(OwnerDeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")
   
class BlogPostCreateView(OwnerCreateView):
    model = BlogPost
    fields = ["title", "text", "status"]
    success_url = reverse_lazy("blog_app:posts")
    
class BlogUpdateView(OwnerUpdateView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")
    fields = ["title", "text", "status"]