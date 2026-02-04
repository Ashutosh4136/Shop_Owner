from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='admin_dashboard'),
    path('dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('orders/', views.order_list_view, name='admin_order_list'),
    path('orders/<int:order_id>/update/', views.update_order_status, name='admin_update_order_status'),
]
