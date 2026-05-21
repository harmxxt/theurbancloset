from django.urls import path
from . import views

urlpatterns = [
    path('<str:invoice_number>/', views.invoice_detail, name='invoice_detail'),
    path('<str:invoice_number>/download/', views.download_invoice, name='download_invoice'),
    path('admin/list/', views.admin_invoice_list, name='admin_invoice_list'),
    path('admin/create/<int:order_id>/', views.manually_create_invoice, name='manually_create_invoice'),
]
