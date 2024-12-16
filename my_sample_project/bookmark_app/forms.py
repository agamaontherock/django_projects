from django import forms
from .models import Image
from django.utils.text import slugify
from django.core.files.base import ContentFile
import requests

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'description', 'url']
        widgets = {
            'url' : forms.HiddenInput 
        }
        
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        
        return url
    
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        extension = image_url.rsplit('.', 1)[1].lower()
        slug = slugify(self.cleaned_data['title'])
        file_name = f'{slug}.{extension}'
        
        response = requests.get(image_url)          
        image.image.save(
            file_name,
            ContentFile(response.content),
            save=False
        )
        
        if commit:
            image.save()
            
        return image