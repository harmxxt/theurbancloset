from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Product categories like Men, Women, Shirts, etc."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    # Color for category badge on frontend
    color = models.CharField(max_length=20, default='#C9A96E')

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_products', kwargs={'slug': self.slug})


class Product(models.Model):
    """Luxury clothing product"""
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Discounted price (optional)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)
    # Product image - we use URL for placeholder images
    image_url = models.URLField(max_length=500, blank=True, default='')
    # Available sizes
    sizes = models.CharField(max_length=100, default='XS,S,M,L,XL,XXL', help_text='Comma-separated sizes')
    # Material/fabric
    material = models.CharField(max_length=100, blank=True)
    # Brand (all TheUrbanCloset but can vary)
    brand = models.CharField(max_length=100, default='TheUrbanCloset')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_display_price(self):
        """Returns discounted price if available, else regular price"""
        return self.discount_price if self.discount_price else self.price

    def get_savings(self):
        """Returns amount saved if discounted"""
        if self.discount_price:
            return self.price - self.discount_price
        return 0

    def get_discount_percent(self):
        """Returns discount percentage"""
        if self.discount_price and self.price > 0:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

    def is_low_stock(self):
        """Flag low stock items"""
        return self.stock <= 5

    def get_sizes_list(self):
        """Returns sizes as a list"""
        return [s.strip() for s in self.sizes.split(',') if s.strip()]
