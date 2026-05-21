from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'amount', 'date', 'added_by']
    list_filter = ['category', 'date']
    search_fields = ['title', 'description']
