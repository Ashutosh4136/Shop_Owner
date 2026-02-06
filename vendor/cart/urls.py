from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail_view, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('increase/<int:product_id>/', views.increase_qty, name="increase_qty"),
    path('decrease/<int:product_id>/', views.decrease_qty, name="decrease_qty"),
    path('remove/<int:product_id>/', views.remove_from_cart_view, name='remove_from_cart'),
]
