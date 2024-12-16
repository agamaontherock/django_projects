from . import views
from django.urls import path

app_name = 'images'

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create/", views.image_create, name="create")
]