from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from products.models import Product
from .models import WishlistItem, Wishlist
from .utils import get_or_create_wishlist

@login_required(login_url='login')
def wishlist_view(request):
    wishlist = get_or_create_wishlist(request.user)
    items = wishlist.items.select_related('product')
    return render(request, 'wishlist.html', {'items': items})


def add_to_wishlist(request, product_id):
    wishlist = get_or_create_wishlist(request.user)
    product = get_object_or_404(Product, id=product_id)

    WishlistItem.objects.get_or_create(
        wishlist=wishlist,
        product=product
    )

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
def remove_from_wishlist(request, item_id):
    item = get_object_or_404(WishlistItem, id=item_id, wishlist__user=request.user)
    item.delete()
    
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        wishlist = get_or_create_wishlist(request.user)
        return JsonResponse({
            "success": True,
            "count": wishlist.items.count()
        })
    
    return redirect('wishlist')


@login_required(login_url='login')
def remove_from_wishlist_by_product(request, product_id):
    WishlistItem.objects.filter(
        wishlist__user=request.user,
        product_id=product_id
    ).delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def toggle_wishlist_ajax(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        wishlist = get_or_create_wishlist(request.user)

        item = WishlistItem.objects.filter(
            wishlist=wishlist,
            product=product
        ).first()

        if item:
            item.delete()
            status = "removed"
        else:
            WishlistItem.objects.create(
                wishlist=wishlist,
                product=product
            )
            status = "added"

        count = wishlist.items.count()

        return JsonResponse({
            "status": status,
            "count": count,
            "success": True
        })
    
    return JsonResponse({"error": "Invalid request"}, status=400)

