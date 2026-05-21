from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('inventory/', views.inventory_management, name='inventory_management'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/delete/<int:pk>/', views.expense_delete, name='expense_delete'),
    path('reports/', views.reports, name='reports'),
]
