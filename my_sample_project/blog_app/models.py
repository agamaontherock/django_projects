from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    blogpost = models.ForeignKey(BlogPost, related_name="comments", on_delete=models.CASCADE)
    post_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    