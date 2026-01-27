from .models import CartItem
from django.db import models
from .utils import get_or_create_user_cart, get_or_create_session_cart

def cart_count(request):
    if request.user.is_authenticated:
        cart = get_or_create_user_cart(request.user)
    else:
        cart = get_or_create_session_cart(request)

    count = CartItem.objects.filter(cart=cart).aggregate(
        total_quantity=models.Sum('quantity')
    )['total_quantity'] or 0

    return {'cart_count': count}
