from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='admin_dashboard'),
    path('orders/', views.order_list_view, name='admin_order_list'),
    path('orders/<int:order_id>/update/', views.update_order_status, name='admin_update_order_status'),
]
