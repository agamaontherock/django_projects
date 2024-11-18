from django.db import models
from django.conf import settings
from django.core.validators import *
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User

class PublishedPostsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=BlogPost.Status.PUBLISHED)
    
class BlogPost(models.Model):
    class Status(models.TextChoices):
        DRAFT = "D", "Draft"
        PUBLISHED = "P", "Published"
        
    title = models.CharField(max_length=200, validators=[MinLengthValidator(10)])
    text = models.TextField(validators=[MinLengthValidator(10)])
    slug = models.SlugField(unique_for_date = 'created_at')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True, default=None)
    status = models.CharField(
        max_length=1,
        choices=Status,
        default=Status.DRAFT,
    )
    
    # Managers
    objects = models.Manager()
    published_objects = PublishedPostsManager()
    
    def save(self, *args, **kwargs):
        if self.pk:
            previous = BlogPost.objects.get(pk=self.pk)
            if previous.status == BlogPost.Status.DRAFT and \
                self.status == BlogPost.Status.PUBLISHED:
            
                self.published_at = timezone.now()
            else:
                self.published_at = None
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)    
    
    def get_absolute_url(self):
        return reverse(
            'blog_app:post_by_slug',
            args=[
                self.created_at.year,
                self.created_at.month,
                self.created_at.day,
                self.slug
                ]
            )
        # return reverse("blog_app:post", kwargs={"pk": self.pk})
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, 
                             related_name="comments")
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)