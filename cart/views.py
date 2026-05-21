from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from decimal import Decimal
from products.models import Product
from .models import Cart, CartItem


@login_required
def cart_detail(request):
    """View cart"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')

    tax_rate = Decimal(str(settings.TAX_RATE))
    delivery = Decimal(str(settings.DELIVERY_CHARGE))
    subtotal = cart.get_total()
    tax = round(subtotal * tax_rate, 2)
    delivery_charge = delivery if subtotal > 0 else Decimal('0')
    total = subtotal + tax + delivery_charge if subtotal > 0 else Decimal('0')

    context = {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'tax': tax,
        'delivery': delivery_charge,
        'total': total,
    }
    return render(request, 'cart/cart.html', context)


@login_required
def add_to_cart(request, product_id):
    """Add product to cart — handles both GET (quick-add) and POST (detail page with size/qty)"""
    product = get_object_or_404(Product, id=product_id, is_active=True)

    if product.stock <= 0:
        messages.error(request, f'Sorry, {product.name} is out of stock.')
        return redirect('product_detail', slug=product.slug)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Read from POST if available, else defaults
    data = request.POST if request.method == 'POST' else request.GET
    size = data.get('size', '')
    try:
        quantity = max(1, int(data.get('quantity', 1)))
    except (ValueError, TypeError):
        quantity = 1

    # Prevent adding more than available stock
    existing_qty = CartItem.objects.filter(
        cart=cart, product=product, size=size
    ).values_list('quantity', flat=True).first() or 0

    if existing_qty + quantity > product.stock:
        messages.warning(request, f'Only {product.stock} units of {product.name} are available.')
        return redirect('product_detail', slug=product.slug)

    item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, size=size,
        defaults={'quantity': quantity}
    )
    if not created:
        item.quantity += quantity
        item.save()

    messages.success(request, f'✓ {product.name} added to your cart!')
    return redirect('cart_detail')


@login_required
def update_cart(request, item_id):
    """Update cart item quantity"""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1

    if quantity <= 0:
        item.delete()
        messages.info(request, 'Item removed from cart.')
    else:
        item.quantity = quantity
        item.save()
        messages.success(request, 'Cart updated.')
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, item_id):
    """Remove item from cart"""
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = item.product.name
    item.delete()
    messages.info(request, f'{product_name} removed from cart.')
    return redirect('cart_detail')


@login_required
def clear_cart(request):
    """Remove all items from cart"""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.items.all().delete()
    messages.info(request, 'Your cart has been cleared.')
    return redirect('cart_detail')
