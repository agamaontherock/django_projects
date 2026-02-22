from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Message(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    message = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
       return f'{self.user} on {self.topic} at {self.sent_on}'