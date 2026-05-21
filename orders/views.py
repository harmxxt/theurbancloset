from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from decimal import Decimal

from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items   = cart.items.select_related('product')

    if not items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart_detail')

    subtotal = cart.get_total()
    tax      = round(subtotal * Decimal(str(settings.TAX_RATE)), 2)
    delivery = Decimal(str(settings.DELIVERY_CHARGE))
    total    = subtotal + tax + delivery

    if request.method == 'POST':
        form = CheckoutForm(request.POST, user=request.user)
        if form.is_valid():
            # ── Step 1: save the order header ──────────────────────────
            order = form.save(commit=False)
            order.user           = request.user
            order.subtotal       = subtotal
            order.tax_amount     = tax
            order.delivery_charge= delivery
            order.total_amount   = round(total, 2)
            if order.payment_method == 'demo':
                order.payment_status = 'paid'
                order.status         = 'confirmed'
            order.save()                       # signal does NOT generate invoice here

            # ── Step 2: create all order items ─────────────────────────
            for cart_item in items:
                OrderItem.objects.create(
                    order         = order,
                    product       = cart_item.product,
                    product_name  = cart_item.product.name,
                    product_price = cart_item.product.get_display_price(),
                    quantity      = cart_item.quantity,
                    size          = cart_item.size,
                )
                # Reduce stock
                p = cart_item.product
                p.stock = max(0, p.stock - cart_item.quantity)
                p.save()

            # ── Step 3: clear cart ─────────────────────────────────────
            items.delete()

            # ── Step 4: NOW generate invoice (items exist in DB) ───────
            try:
                from invoices.services import create_invoice_for_order
                create_invoice_for_order(order)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(
                    f"Invoice generation failed for {order.order_number}: {e}"
                )
                # Order is already saved — don't block the customer

            messages.success(
                request,
                f'Order {order.order_number} placed! '
                f'Check your email for the invoice.'
            )
            return redirect('order_success', order_number=order.order_number)
        else:
            messages.error(request, 'Please fill in all required fields correctly.')
    else:
        form = CheckoutForm(user=request.user)

    context = {
        'form'    : form,
        'items'   : items,
        'subtotal': subtotal,
        'tax'     : tax,
        'delivery': delivery,
        'total'   : round(total, 2),
    }
    return render(request, 'orders/checkout.html', context)


@login_required
def order_success(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': order.items.all(),
    })
