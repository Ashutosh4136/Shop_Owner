from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('search/', views.product_search, name='product_search'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
