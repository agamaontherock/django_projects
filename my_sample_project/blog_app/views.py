from django.shortcuts import get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic import DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from django.core.mail import send_mail

from .models import BlogPost
from .forms import CommentForm, EmailForm

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
    paginate_by = 5
    queryset = BlogPost.published_objects.all()
    
class MyPostsListView(ListView):
    model = BlogPost
    paginate_by = 5
    queryset = BlogPost.objects.all()
    
    def get_queryset(self, **kwargs):
       qs = BlogPost.objects.filter(owner = self.request.user)
       return qs
    
class BlogDetailView(DetailView):
    model = BlogPost
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['form'] = CommentForm()
        ctx['email_form'] = EmailForm()
        return ctx
    
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
    fields = ["title", "text", "status"]
    
    def get_queryset(self, **kwargs):
       qset = super().get_queryset(**kwargs)
       qset = qset.filter(owner = self.request.user)
       return qset
    
class BlogDeleteView(DeleteView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")
    
@require_POST
def comment_post(request, post_id):
    form = CommentForm(request.POST)
    post_obj = get_object_or_404(BlogPost, id = post_id)
    
    comment = None
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post_obj
        comment.user = request.user
        comment.save()
        
    return redirect(post_obj)

@require_POST
def share_post(request, post_id):
    post_obj = get_object_or_404(BlogPost, id = post_id)
    post_abs_url = post_obj.get_absolute_url()
    
    form = EmailForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        data.text += f"Post url: {post_abs_url}"
        send_mail(
            data.subject,
            data.text,
            "agamaontherock@gmail.com",
            [data.to],
            fail_silently=False,
        )
        print(f"@@@ Sending email to {data}")
    
    return redirect(post_obj)