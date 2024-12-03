from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import *
from .models import Profile

# Create your views here.
def home(request):
    return render(request, "home_app/home.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request,
                  user,
                  backend='home_app.authentication.EmailAuthBackend')  # Log in the user immediately after registration
            return redirect('home_app:home')  # Redirect to a 'home' page after registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def open_page(request):
    return HttpResponse("<h1>Open page</h1><p> This page is available to everyone without any restrictions. Enjoy!</p>")

@login_required
def closed_page(request):
    return HttpResponse("<h1>Closed page</h1><p>This page is available only to authorized users. <br> You are definitely authorized if you see this page.</p>")

@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request, 
                  'registration/account_edit.html',
                  {"user_form" : user_form, 
                   "profile_form": profile_form 
    })
