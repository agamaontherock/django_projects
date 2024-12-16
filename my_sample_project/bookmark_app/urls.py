from . import views
from django.urls import path

app_name = 'images'

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("create/", views.image_create, name="create"),
    path("detail/<int:id>/<slug:slug>", views.image_detail, name="detail")
]