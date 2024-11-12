from django.db import models
from django.conf import settings
from django.core.validators import *
from django.urls import reverse

class BlogPost(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(10)])
    text = models.TextField(validators=[MinLengthValidator(10)])
    slug = models.SlugField(unique_for_date = 'created_at')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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