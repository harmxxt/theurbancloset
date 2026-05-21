from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/category/<slug:slug>/', views.category_products, name='category_products'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
]
