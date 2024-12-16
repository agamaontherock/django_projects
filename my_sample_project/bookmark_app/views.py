from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ImageCreateForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Image

@login_required
def dashboard(request):
    return render(
        request,
        'bookmark_app/dashboard.html',
        {'section': 'dashboard'}
    )
    
@login_required
def image_create(request):
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            # assign current user to the item
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image added successfully')
            # redirect to new created item detail view
            return redirect(new_image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
            
    return render(request,
                 'bookmark_app/image/create.html',
                 {'section': 'images', 'form': form}
                 )
    