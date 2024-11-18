from django.forms import ModelForm, Form
from django import forms
from .models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        

class EmailForm(Form):
    to = forms.EmailField()
    subject = forms.CharField()
    text  = forms.CharField(widget=forms.Textarea)
    