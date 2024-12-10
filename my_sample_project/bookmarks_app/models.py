from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

class Image(models.Model):
    url = models.URLField(max_length=2000)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='images_liked',
        blank=True
    )
    
    class Meta:
        indexes = [
            models.Index(fields=['-created_at']),
        ]
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("images:details",
                       kwargs={"id": self.id, "slug": self.slug})
    