from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    """Shopping cart linked to user"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def get_total(self):
        """Total price of all items in cart"""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_item_count(self):
        """Total number of items"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Individual item in cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'product', 'size']

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_subtotal(self):
        """Price x quantity for this item"""
        return self.product.get_display_price() * self.quantity
