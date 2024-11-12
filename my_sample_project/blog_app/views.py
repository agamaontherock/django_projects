from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from .models import BlogPost
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.utils.text import slugify

class BlogPostCreateView(LoginRequiredMixin, CreateView):
    model = BlogPost
    fields = ["title", "text"]

    # Saves the form instance, sets the current object for the view, and redirects to get_success_url().
    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.slug = slugify(object.title)
        object.save()
        return super(BlogPostCreateView, self).form_valid(form)
    
class BlogListView(ListView):
    model = BlogPost
    paginate_by = 2
    
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
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk")
        
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        slug_id = self.kwargs.get("slug_id")

        if pk:
            return get_object_or_404(self.model, pk=pk)
        elif slug_id:
            return get_object_or_404(self.model, 
                                     created_at__year=year, 
                                     created_at__month=month, 
                                     created_at__day=day, 
                                     slug = slug_id)
        else:
            raise Http404("No object found matching the provided criteria.")

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