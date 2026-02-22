from django.urls import path
from . import views
# from django.conf.urls import url

app_name = 'shop'
urlpatterns = [
    path('', views.product_list, name='product_list'),
    path(
        '<slug:category_slug>/',
        views.product_list,
        name='product_list_by_category',
    ),
    path(
        '<int:id>/<slug:slug>/',
        views.product_detail,
        name='product_detail',
    ),
    path('cart/detail/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('order/create/', views.order_create, name='order_create'),
    
    path('payment/process/', views.payment_process, name='payment_process'),
    path('payment/completed/', views.payment_completed, name='payment_completed'),
    path('payment/canceled/', views.payment_canceled, name='payment_canceled'),
    
    # url(r'^pay/$', views.PayView.as_view(), name='pay_view'),
    # url(r'^pay-callback/$', views.PayCallbackView.as_view(), name='pay_callback'),
]
