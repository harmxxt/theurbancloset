from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'order', 'status', 'pdf_generated', 'email_sent', 'issued_date']
    list_filter  = ['status', 'pdf_generated', 'email_sent']
    search_fields = ['invoice_number', 'order__order_number']
    readonly_fields = ['invoice_number', 'pdf_generated', 'email_sent']
