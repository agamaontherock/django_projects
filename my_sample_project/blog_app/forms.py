from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
class EmailForm(forms.Form):
    email_to = forms.EmailField()
    subject = forms.CharField(max_length=120)
    text = forms.CharField(widget=forms.Textarea)