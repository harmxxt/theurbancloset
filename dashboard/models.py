from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):
    """Track business expenses"""
    CATEGORY_CHOICES = [
        ('inventory', 'Inventory Purchase'),
        ('shipping', 'Shipping & Logistics'),
        ('marketing', 'Marketing & Advertising'),
        ('utilities', 'Utilities'),
        ('salaries', 'Salaries'),
        ('rent', 'Rent'),
        ('technology', 'Technology'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"
