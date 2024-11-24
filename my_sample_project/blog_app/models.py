from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from taggit.managers import TaggableManager

class PublishedPostsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=BlogPost.PublicationStatus.PUBLISHED)

        
class BlogPost(models.Model):
    class Meta:
        ordering = ['-published_at']
    
    class PublicationStatus(models.TextChoices):
        DRAFT = "D", _("Draft")
        PUBLISHED = "P", _("Published")

    status = models.CharField(
        max_length=1,
        choices=PublicationStatus,
        default=PublicationStatus.DRAFT,
    )
    
    title = models.CharField(max_length=100)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique_for_date = 'created_at', blank=False)
    published_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()
    published_objects = PublishedPostsManager()
    
    tags = TaggableManager()
    
    def __str__(self):
        return self.title + " | by " + self.owner.username
    
    def get_absolute_url(self):
        # return reverse("post/<int:pk>", kwargs={"pk": self.pk})
        return reverse(
            'blog_app:post',
            args=[
                self.created_at.year,
                self.created_at.month,
                self.created_at.day,
                self.slug
                ]
            )
    
    def save(self, *args, **kwargs):
        if self.pk:
            previous = BlogPost.objects.get(pk=self.pk)
            if previous.status == BlogPost.PublicationStatus.DRAFT and \
                self.status == BlogPost.PublicationStatus.PUBLISHED:
            
                self.published_at = timezone.now()
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_at']
        indexes = [models.Index(fields=['created_at']),]
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'