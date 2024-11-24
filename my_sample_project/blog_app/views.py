from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.mail import send_mail
from django.core.paginator import Paginator

from taggit.models import Tag
from django.db.models import Count

from .ownerviews import *
from .forms import *
from .models import BlogPost

class BlogListView(ListView):
    model = BlogPost
    paginate_by = 5
    queryset = BlogPost.published_objects.all()
    
    def get_queryset(self):
        tag_slug = self.request.GET.get('tag_slug', None)
        
        if (tag_slug):
            tag = get_object_or_404(Tag, slug=tag_slug)
            return super().get_queryset().filter(tags__in=[tag])
        
        return super().get_queryset().all()
    
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
        
        post = ctx["blogpost"]
        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = BlogPost.published_objects.filter(
            tags__in=post_tags_ids
        ).exclude(id=post.id)
        similar_posts = similar_posts.annotate(
            same_tags=Count('tags')
        ).order_by('-same_tags', '-published_at')[:4]
        ctx["similar_posts"] = similar_posts

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
    fields = ["title", "text", "status", "tags"]
    success_url = reverse_lazy("blog_app:posts")
    
class BlogUpdateView(OwnerUpdateView):
    model = BlogPost
    success_url = reverse_lazy("blog_app:posts")
    fields = ["title", "text", "status", "tags"]
    
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

def post_list_by_tag(request, tag_slug=None):
    post_list = BlogPost.published_objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog_app/blogpost_list.html',
        {
            'page_obj': posts,
            'tag': tag
        }
        )
