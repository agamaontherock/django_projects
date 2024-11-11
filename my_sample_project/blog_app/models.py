from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique_for_date = True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
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
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)