from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from cart.utils import get_or_create_user_cart, get_or_create_session_cart
from .models import Product, ProductImage, ProductSize, Category
from django.db.models import Q
from django.db.models.functions import Random
from wishlist.models import WishlistItem


def search(request):
    query = request.GET.get("q", "")
    results = Product.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query),
        is_live=True
    )

    return render(request, "navbar.html", {
        "query": query,
        "results": results
    })


def search_products(request):
    query = request.GET.get("q", "")
    results = Product.objects.filter(name__icontains=query, is_live=True)

    return render(request, "search_results.html", {
        "query": query,
        "results": results
    })

# -----------------------------
# PRODUCTS LIST PAGE
# -----------------------------
def products_page(request):
    sort = request.GET.get('sort', "")
    products = Product.objects.filter(is_live=True)
    category_slug = request.GET.get("category")

    # Get cart based on user authentication
    if request.user.is_authenticated:
        cart = get_or_create_user_cart(request.user)
    else:
        cart = get_or_create_session_cart(request)

    cart_items = cart.items.select_related('product')

    cart_product_map = {
        item.product_id: item.id   # product_id → cart_item_id
        for item in cart_items
    }

    # Filters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_slug:
        products = products.filter(category__slug=category_slug)
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if sort == "price":
        products = products.order_by("price")
    elif sort == "-price":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-created_at")
    elif sort == "random":
        products = products.annotate(random_order=Random()).order_by("random_order")
    else:
        # Default: random sort
        products = products.annotate(random_order=Random()).order_by("random_order")
        sort = "random"

    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = WishlistItem.objects.filter(
            wishlist__user=request.user
        ).values_list('product_id', flat=True)
    
    categories = Category.objects.all()

    paginator = Paginator(products, 8)
    page = request.GET.get("page")
    products = paginator.get_page(page)

    return render(request, "products.html", {
        "products": products,
        'wishlist_product_ids': wishlist_product_ids,
        "cart_product_map": cart_product_map, 
        "sort": sort,
        "categories": categories
    })




# -----------------------------
# PRODUCT DETAILS PAGE
# -----------------------------
def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug, is_live=True)

    # all gallery images
    gallery = ProductImage.objects.filter(product=product)

    # sizes (only if created for this product)
    sizes = ProductSize.objects.filter(product=product)

    # Get cart based on user authentication
    if request.user.is_authenticated:
        cart = get_or_create_user_cart(request.user)
    else:
        cart = get_or_create_session_cart(request)

    cart_items = cart.items.select_related('product')

    cart_product_map = {
        item.product_id: item.id   # product_id → cart_item_id
        for item in cart_items
    }

    # related products: same category, exclude itself
    related_products = Product.objects.filter(
        category=product.category,
        is_live=True
    ).exclude(id=product.id)[:16]   # limit 16

    wishlist_product_ids = []
    if request.user.is_authenticated:
        wishlist_product_ids = WishlistItem.objects.filter(
            wishlist__user=request.user
        ).values_list('product_id', flat=True)


    context = {
        "product": product,
        "gallery": gallery,
        "sizes": sizes,
        "related_products": related_products,
        'wishlist_product_ids': wishlist_product_ids,
        "cart_product_map": cart_product_map,
    }

    return render(request, "product_details.html", context)
