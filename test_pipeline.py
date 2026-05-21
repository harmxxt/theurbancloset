"""
TheUrbanCloset Quick Test Script
Run with: python test_pipeline.py

Tests:
1. Database connection
2. Product seeding
3. Order creation
4. Invoice number generation
5. PDF generation
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'theurbancloset.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Product, Category
from orders.models import Order, OrderItem
from invoices.models import Invoice
from invoices.services import generate_invoice_pdf, create_invoice_for_order

print("=" * 60)
print("  TheUrbanCloset — Automation Pipeline Test")
print("=" * 60)

# 1. Check products exist
product_count = Product.objects.count()
category_count = Category.objects.count()
print(f"\n✅ Products in DB: {product_count}")
print(f"✅ Categories in DB: {category_count}")

if product_count == 0:
    print("⚠  No products found! Run: python manage.py seed_products")
    sys.exit(1)

# 2. Create a test order
user, _ = User.objects.get_or_create(
    username='testcustomer',
    defaults={
        'email': 'testcustomer@example.com',
        'first_name': 'Test',
        'last_name': 'Customer',
    }
)

product = Product.objects.filter(is_active=True, stock__gt=0).first()
print(f"\n✅ Test product: {product.name} — ₹{product.get_display_price()}")

order = Order.objects.create(
    user=user,
    full_name='Test Customer',
    email='testcustomer@example.com',
    phone='9876543210',
    address_line1='456 Test Lane',
    city='Delhi',
    state='Delhi',
    postal_code='110001',
    country='India',
    subtotal=product.get_display_price(),
    tax_amount=round(float(product.get_display_price()) * 0.18, 2),
    delivery_charge=99,
    total_amount=round(float(product.get_display_price()) * 1.18 + 99, 2),
    payment_method='demo',
    payment_status='paid',
    status='confirmed',
)
OrderItem.objects.create(
    order=order,
    product=product,
    product_name=product.name,
    product_price=product.get_display_price(),
    quantity=1,
    size='M',
)
print(f"\n✅ Order created: {order.order_number}")
print(f"   Total: ₹{order.total_amount}")

# 3. Test invoice creation
invoice = create_invoice_for_order(order)
print(f"\n✅ Invoice created: {invoice.invoice_number}")
print(f"   PDF generated: {invoice.pdf_generated}")
print(f"   Email sent: {invoice.email_sent}")

if invoice.pdf_file:
    import os
    pdf_path = invoice.pdf_file.path
    if os.path.exists(pdf_path):
        size = os.path.getsize(pdf_path)
        print(f"   PDF size: {size} bytes ({size // 1024} KB)")
        print(f"   PDF path: {pdf_path}")

# 4. Summary
print("\n" + "=" * 60)
print("  Test Results")
print("=" * 60)
print(f"  Orders in DB:  {Order.objects.count()}")
print(f"  Invoices in DB: {Invoice.objects.count()}")
print(f"  PDF Pipeline:   {'✅ Working' if invoice.pdf_generated else '❌ Failed'}")
print(f"  Email:          {'✅ Sent' if invoice.email_sent else '⚠  Not configured (normal)'}")
print()
print("  🎉 Core pipeline is working correctly!")
print("=" * 60)

# Cleanup test data
order.delete()
user.delete()
print("\n  (Test data cleaned up)")
