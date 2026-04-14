from django.shortcuts import render
from products.models import Product, Category
from .models import ThemeSettings
from cart.utils import get_or_create_user_cart
from wishlist.models import WishlistItem


def index(request):
    # Theme from admin
    theme = ThemeSettings.objects.all()

    # Featured products
    featured = Product.objects.filter(is_live=True, is_featured=True)

    # Latest products
    latest = Product.objects.filter(is_live=True).order_by('-created_at')[:8]

    # All categories
    categories = Category.objects.all()

    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = WishlistItem.objects.filter(
            wishlist__user=request.user
        ).values_list('product_id', flat=True)



    # All products (if you still need it)
    products = Product.objects.all()

    return render(request, 'index.html', {
        'products': products,
        'featured': featured,
        'latest': latest,
        'categories': categories,
        'theme': theme,
        'wishlist_product_ids': wishlist_product_ids,
    })


