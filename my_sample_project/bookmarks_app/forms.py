from django import forms
from .models import Image
import requests
from django.utils.text import slugify
from django.core.files.base import ContentFile

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'description', 'url']
        widgets = {
            'url' : forms.HiddenInput
        }
        
    def clean_url(self):
        url = self.cleaned_data['url']
        extention = url.rsplit('.')[-1].lower()
        allowed_extensions = ['png', 'jpg', 'jpeg']
        if extention not in allowed_extensions:
            raise forms.ValidationError('Wrong image file extention')
        
        return url
    
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        
        url = self.cleaned_data['url']
        title = self.cleaned_data['title']
        name = slugify(title)
        extension = url.rsplit('.',1)[-1].lower()
        image_name = f'{name}.{extension}'
        
        response = requests.get(url)
        image.image.save(
            image_name,
            ContentFile(response.content),
            save = False
        )
        
        if commit:
            image.save()
        
        return image