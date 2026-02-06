from django.urls import path
from . import views

urlpatterns = [
    path('dashboard1/', views.dashboard_view, name='admin_dashboard'),
    path('dashboard2/', views.vendor_dashboard, name='vendor_dashboard'),
    path("orders/", views.vendor_orders, name="vendor_orders"),
    path('products/', views.vendor_products, name='vendor_products'),
    path("products/edit/<int:id>/", views.edit_product, name="vendor_edit_product"),
    path("products/delete/<int:id>/", views.delete_product, name="vendor_delete_product"),
    path('dashboard3/', views.customer_dashboard, name='customer_dashboard'),
    path('orders/', views.order_list_view, name='admin_order_list'),
    path('orders/<int:order_id>/update/', views.update_order_status, name='admin_update_order_status'),
]
