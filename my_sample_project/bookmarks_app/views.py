from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ImageCreateForm
from .models import Image

@login_required
def create_image(request):
    if request.method == 'POST':
        form = ImageCreateForm(data = request.POST)
        if form.is_valid():
            image = form.save(commit = False)
            image.user = request.user
            image.save()
            
            return redirect(image.get_absolute_url())
    else:
        form = ImageCreateForm(data = request.GET)
        
    return render(request, 
                  'bookmarks_app/image/create.html', 
                  {
                      'section': 'images',
                      'form': form
                  }
                  )
    
@login_required
def image_details(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 
                  "bookmarks_app/image/details.html", 
                  {"image": image, "section" : "images"})
    
@login_required
def dashboard(request):
    return render(request, "bookmarks_app/dashboard.html")