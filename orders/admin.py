from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_price', 'quantity', 'size', 'get_subtotal']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'full_name', 'status', 'payment_status', 'total_amount', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method']
    list_editable = ['status', 'payment_status']
    search_fields = ['order_number', 'full_name', 'email']
    readonly_fields = ['order_number', 'subtotal', 'tax_amount', 'delivery_charge', 'total_amount']
    inlines = [OrderItemInline]
    ordering = ['-created_at']
