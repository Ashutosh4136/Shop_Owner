from django.urls import path
from . import views

urlpatterns = [
    path('add/<slug:product_slug>/', views.add_review, name='add_review'),
]
