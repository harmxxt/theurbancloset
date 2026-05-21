from django.db import models
from orders.models import Order
import uuid


def generate_invoice_number():
    """Generate unique invoice number like INV-2024-XXXXX"""
    from django.utils import timezone
    year = timezone.now().year
    unique = str(uuid.uuid4()).upper()[:6]
    return f"INV-{year}-{unique}"


class Invoice(models.Model):
    """Invoice linked to an order"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('issued', 'Issued'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='issued')

    # PDF file stored locally
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)

    # Track automation steps
    pdf_generated = models.BooleanField(default=False)
    email_sent = models.BooleanField(default=False)

    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            self.invoice_number = generate_invoice_number()
        super().save(*args, **kwargs)

    def get_download_url(self):
        """Returns local file URL for invoice PDF"""
        if self.pdf_file:
            return self.pdf_file.url
        return None
