from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import BlogPost

class BlogListView(ListView):
    model = BlogPost

class BlogDetailView(DetailView):
    model = BlogPost
    
class BlogDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")
    
    def get_queryset(self, **kwargs):
        qset = super().get_queryset(**kwargs)
        qset = qset.filter(owner = self.request.user)
        return qset
    
class BlogUpdateView(UpdateView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")
    fields = ["title", "text"]
    # fields = "__all__"
    
    def get_queryset(self, **kwargs):
        qset = super().get_queryset(**kwargs)
        qset = qset.filter(owner = self.request.user)
        return qset