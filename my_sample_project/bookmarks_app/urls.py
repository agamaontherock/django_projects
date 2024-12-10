from django.urls import path
from . import views 

app_name = "images" 

urlpatterns = [
    path('create/', views.create_image, name = 'create'),
    path('details/<int:id>/<slug:slug>', views.image_details, name = 'details'),
    path('dashboard/', views.dashboard, name="dashboard")
]
