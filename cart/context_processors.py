from .models import Cart


def cart_count(request):
    """Inject cart item count into all templates"""
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.get_item_count()
        except Cart.DoesNotExist:
            count = 0
    return {'cart_count': count}
