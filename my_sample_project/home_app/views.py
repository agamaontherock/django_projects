from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login

# Create your views here.
def home(request):
    return render(request, "home_app/home.html")

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately after registration
            return redirect('home_app:home')  # Redirect to a 'home' page after registration
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def open_page(request):
    return HttpResponse("<h1>Open page</h1><p> This page is available to everyone without any restrictions. Enjoy!</p>")

@login_required
def closed_page(request):
    return HttpResponse("<h1>Closed page</h1><p>This page is available only to authorized users. <br> You are definitely authorized if you see this page.</p>")

def edit_account(request):
    return render(request, 
                  'registration/account_edit.html',
                  {
                      
                  })