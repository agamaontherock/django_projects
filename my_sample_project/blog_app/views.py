from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.mail import send_mail
from django.contrib import messages

from .ownerviews import *
from .forms import *
from .models import BlogPost

class BlogListView(ListView):
    model = BlogPost
    paginate_by = 5
    queryset = BlogPost.published_objects.all()
    
class MyPostsListView(ListView):
    model = BlogPost
    paginate_by = 5
    
    def get_queryset(self):
        return super().get_queryset().filter(owner = self.request.user)

class BlogDetailView(DetailView):
    model = BlogPost
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comment_form"] = CommentForm()
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
    
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id) #,status=BlogPost.PublicationStatus.PUBLISHED
    comment = None

    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.blogpost = post
        comment.user = request.user
        comment.save()
        
        messages.add_message(request, messages.WARNING, "Comment was added.")
        
    return render(request,
                  'blog_app/comment.html',
                  {
                    'blogpost': post,
                    'form': form,
                    'comment': comment
                  }
                  )
    
def share_by_email(request, post_id):
    form = None
    if request.method == "POST":
        form = EmailForm(request.POST)
        if (form.is_valid()):
            email_to = form.cleaned_data["email_to"]
            subject = form.cleaned_data["subject"]
            text = form.cleaned_data["text"]
            
            send_mail(
                subject,
                text,
                from_email=None,
                recipient_list=[email_to],
                fail_silently=False,
            )    
    else:
        form = EmailForm()
    
    ctx = {"form": form }

    return render(request, "blog_app/share_post.html", ctx)
