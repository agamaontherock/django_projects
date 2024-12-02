from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings

from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Repeat password',
        widget= forms.PasswordInput
    )
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']
    
class EditUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
        
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']