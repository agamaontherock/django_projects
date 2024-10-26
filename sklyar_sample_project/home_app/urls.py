from django.urls import path, include
from . import views

app_name = "home_app"

urlpatterns = [
    path('', views.home, name="home"),
    path('index', views.home, name="home"),
    path('register/', views.register, name='register'),
    path('open_page', views.open_page, name="open_page"),    
    path('closed_page', views.closed_page, name="closed_page"),    
    # path('open_page', views.OpenView.as_view(), name='open_page'),
    # path('apereo', views.ApereoView.as_view(), name='apereo'),
    # path('manual', views.ManualProtect.as_view(), name='manual'),
    # path('protect', views.ProtectView.as_view(), name='protect'),
    # path('python', views.DumpPython.as_view(), name='python'),
]
