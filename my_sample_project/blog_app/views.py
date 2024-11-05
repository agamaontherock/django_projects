from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from .models import BlogPost
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    """
    Sub-class of the CreateView to automatically pass the Request to the Form
    and add the owner to the saved object.
    """

    # Saves the form instance, sets the current object for the view, and redirects to get_success_url().
    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(BlogPostCreateView, self).form_valid(form)
    
class BlogListView(ListView):
    model = BlogPost
    
    # def get_queryset(self, **kwargs):
    #    crazy = BlogPost.objects.filter(title__startswith = "Q") # Convention: Car
    #    return crazy

    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['crazy_thing'] = 'CRAZY THING'
    #    print(context)
    #    return context
    
class BlogDetailView(DetailView):
    model = BlogPost

class BlogUpdateView(UpdateView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")
    fields = ["title", "text"]
    
    def get_queryset(self, **kwargs):
       qset = super().get_queryset(**kwargs)
       qset = qset.filter(owner = self.request.user)
       return qset
    
class BlogDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")