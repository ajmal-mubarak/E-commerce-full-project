from cart.utils import get_or_create_user_cart, get_or_create_session_cart
from wishlist.utils import get_or_create_wishlist

def cart_and_wishlist_count(request):
    cart_count = 0
    wishlist_count = 0

    if request.user.is_authenticated:
        cart = get_or_create_user_cart(request.user)
        wishlist = get_or_create_wishlist(request.user)
        cart_count = cart.items.count()
        wishlist_count = wishlist.items.count()
    else:
        cart = get_or_create_session_cart(request)
        cart_count = cart.items.count()

    return {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    }
