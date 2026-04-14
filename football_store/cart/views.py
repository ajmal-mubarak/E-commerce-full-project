import json
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from django.views.decorators.cache import never_cache
from .utils import get_or_create_user_cart, get_or_create_session_cart
from django.utils import timezone
from .models import Coupon
from django.http import JsonResponse
from django.db.models import Sum

def get_cart(request):
    return get_or_create_user_cart(request.user) if request.user.is_authenticated else get_or_create_session_cart(request)


def get_available_coupons(request, subtotal, filter_type='all'):
    """Get all available coupons for the user"""
    today = timezone.now().date()
    
    # Base query
    coupons = Coupon.objects.all().order_by('-id')
    
    # Apply Filters
    if filter_type == 'available' or filter_type == 'all' or not filter_type:
        # Show active and not expired
        coupons = coupons.filter(active=True).exclude(expiry_date__lt=today)
    
    # Type filters
    if filter_type == 'percent':
        coupons = coupons.filter(discount_type='percent', active=True)
    elif filter_type == 'amount':
        coupons = coupons.filter(discount_type='amount', active=True)
    elif filter_type == 'free_shipping':
        coupons = coupons.filter(discount_type='free_shipping', active=True)
    
    # Usage filters
    elif filter_type == 'one_time':
        coupons = coupons.filter(one_time_use=True, active=True)

    available_coupons = []
    
    for coupon in coupons:
        # Check if user-specific coupon
        if coupon.users.exists():
            if not request.user.is_authenticated or request.user not in coupon.users.all():
                continue
        
        # Check if already used (one-time use)
        is_used = False
        if coupon.one_time_use and request.user.is_authenticated:
            if request.user in coupon.used_by.all():
                is_used = True
                
        # "Available" filter strict check: exclude used one-time coupons
        if filter_type == 'available' and is_used:
             continue

        # Check eligibility (min spend)
        eligible = subtotal >= coupon.minimum_amount
        
        coupon_info = {
            'id': coupon.id,
            'code': coupon.code,
            'discount_type': coupon.discount_type,
            'discount_value': coupon.discount_value,
            'minimum_amount': coupon.minimum_amount,
            'eligible': eligible,
            'discount_text': get_discount_text(coupon),
            'is_used': is_used  # Add used status to info
        }
        
        available_coupons.append(coupon_info)
    
    return available_coupons


def get_discount_text(coupon):
    """Generate human readable discount text"""
    if coupon.discount_type == 'percent':
        return f"{coupon.discount_value}% OFF"
    elif coupon.discount_type == 'amount':
        return f"₹{coupon.discount_value} OFF"
    elif coupon.discount_type == 'free_shipping':
        return "FREE SHIPPING"
    return "Special Offer"


def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        size = request.POST.get("size", "").strip()

        product = get_object_or_404(Product, id=product_id)
        
        # Size is required - redirect back if not provided
        if not size:
            return redirect("product_details", slug=product.slug)
        
        # Check stock
        if product.stock == 0:
             return redirect("product_details", slug=product.slug)

        cart = get_cart(request)

        # CHECK TOTAL QUANTITY ACROSS ALL VARIANTS
        current_holdings = cart.items.filter(product=product).aggregate(Sum('quantity'))['quantity__sum'] or 0
        if current_holdings + quantity > product.stock:
            from django.contrib import messages
            messages.error(request, f"Only {product.stock} items available (You have {current_holdings} in cart).")
            return redirect("product_details", slug=product.slug)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size
        )

        if created:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity

        cart_item.save()

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            cart_count = cart.items.count()
            return JsonResponse({
                "success": True,
                "cart_count": cart_count
            })

        return redirect("product_details", slug=product.slug)

    return redirect("product_details", slug=product.slug)



def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    # Handle both JSON and Form data
    if request.headers.get('content-type') == 'application/json':
        try:
            data = json.loads(request.body)
            quantity = int(data.get("quantity", 1))
        except json.JSONDecodeError:
            quantity = 1
    else:
        quantity = int(request.POST.get("quantity", 1))

    if quantity > 0:
        # CHECK TOTAL QUANTITY ACROSS ALL VARIANTS (EXCLUDING THIS ITEM)
        other_items_qty = CartItem.objects.filter(
            cart=cart_item.cart, 
            product=cart_item.product
        ).exclude(id=item_id).aggregate(Sum('quantity'))['quantity__sum'] or 0
        
        if other_items_qty + quantity > cart_item.product.stock:
            msg = f"Only {cart_item.product.stock} items available."
            if other_items_qty > 0:
                msg += f" (You have {other_items_qty} other variants in cart)"
                
            # If AJAX request, we can return error
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return JsonResponse({"error": msg}, status=400)
            
            # If normal request (fallback), stick to max possible
            quantity = max(0, cart_item.product.stock - other_items_qty)

        cart_item.quantity = quantity
        cart_item.save()

    cart = cart_item.cart
    subtotal = sum(i.quantity * i.product.price for i in cart.items.all())
    
    # Calculate available stock for this item after update
    other_items_qty = CartItem.objects.filter(
        cart=cart_item.cart,
        product=cart_item.product
    ).exclude(id=item_id).aggregate(Sum('quantity'))['quantity__sum'] or 0
    # Ensure available stock is at least the current quantity and never negative
    available_stock = max(cart_item.quantity, cart_item.product.stock - other_items_qty)

    # Calculate correct total with shipping and discount
    discount = 0
    shipping_fee = 12
    coupon_id = request.session.get('coupon_id')
    
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id, active=True)
            if coupon.discount_type == 'percent':
                discount = subtotal * coupon.discount_value / 100
            elif coupon.discount_type == 'amount':
                discount = coupon.discount_value
            elif coupon.discount_type == 'free_shipping':
                shipping_fee = 0
        except Coupon.DoesNotExist:
            pass # Coupon invalid/expired
            
    total = max(subtotal - discount + shipping_fee, 0)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "item_subtotal": cart_item.quantity * cart_item.product.price,
            "item_total": cart_item.quantity * cart_item.product.price,
            "subtotal": subtotal,
            "cart_count": cart.items.count(),
            "total": total,
            "discount": discount,
            "available_stock": available_stock  # Send updated available stock
        })

    return redirect("cart")


def remove_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart = cart_item.cart
    cart_item.delete()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # Calculate new subtotal
        subtotal = sum(i.quantity * i.product.price for i in cart.items.all())
        return JsonResponse({
            "cart_count": cart.items.count(),
            "subtotal": subtotal
        })

    return redirect("cart")


def update_cart_size(request, item_id):
    """Update size for a cart item"""
    if request.method == "POST":
        try:
            cart_item = get_object_or_404(CartItem, id=item_id)
            new_size = request.POST.get("size", "").strip()
            
            if not new_size:
                return JsonResponse({
                    "success": False,
                    "error": "Size cannot be empty"
                }, status=400)
            
            cart_item.size = new_size
            cart_item.save()
            
            return JsonResponse({
                "success": True,
                "size": new_size,
                "message": f"Size updated to {new_size}"
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)
    
    return JsonResponse({
        "success": False,
        "error": "Invalid request method"
    }, status=400)


@never_cache
def cart_page(request):
    # 🔒 Keep your existing logic (unchanged)
    if request.user.is_authenticated:
        cart = get_or_create_user_cart(request.user)
    else:
        cart = get_or_create_session_cart(request)

    items = cart.items.all()

    # Calculate available stock for each item (considering other cart items)
    for item in items:
        # Get quantity of OTHER items with same product
        other_items_qty = CartItem.objects.filter(
            cart=cart,
            product=item.product
        ).exclude(id=item.id).aggregate(Sum('quantity'))['quantity__sum'] or 0
        
        # Calculate max quantity this item can have
        # Ensure it's at least the current quantity (for items already in cart)
        # and never negative
        item.available_stock = max(item.quantity, item.product.stock - other_items_qty)

    # 🔒 Existing subtotal logic
    subtotal = sum(item.quantity * item.product.price for item in items)

    # 🆕 SAFE coupon logic (optional)
    discount = 0
    coupon = None

    coupon_id = request.session.get('coupon_id')

    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id, active=True)

            if coupon.discount_type == 'percent':
                discount = subtotal * coupon.discount_value / 100

            elif coupon.discount_type == 'amount':
                discount = coupon.discount_value

        except Coupon.DoesNotExist:
            request.session.pop('coupon_id', None)

    # Shipping fee logic
    shipping_fee = 12
    if coupon and coupon.discount_type == 'free_shipping':
        shipping_fee = 0

    # 🔒 Final total (safe)
    total = max(subtotal - discount + shipping_fee, 0)

    # Get coupon error if exists
    coupon_error = request.session.get('coupon_error')
    
    # Get available coupons for user
    available_coupons = get_available_coupons(request, subtotal)

    # Render response
    response_data = {
        "cart_items": items,
        "subtotal": subtotal,
        "discount": discount,   # 🆕 optional
        "total": total,
        "coupon": coupon,        # 🆕 optional
        "coupon_error": coupon_error,  # 🆕 error message
        "available_coupons": available_coupons,  # 🆕 available coupons list
        "shipping_fee": shipping_fee  # 🆕 shipping fee
    }
    
    # Clear coupon error after displaying
    if 'coupon_error' in request.session:
        del request.session['coupon_error']
    
    return render(request, "cart.html", response_data)


def apply_coupon(request):
    if request.method == "POST":
        code = request.POST.get("coupon_code", "").strip()

        try:
            coupon = Coupon.objects.get(code__iexact=code, active=True)

            # Expiry check
            if coupon.expiry_date and coupon.expiry_date < timezone.now().date():
                raise Exception("Coupon expired")

            cart = get_cart(request)
            items = cart.items.all()
            subtotal = sum(i.quantity * i.product.price for i in items)

            # Minimum amount check
            if subtotal < coupon.minimum_amount:
                raise Exception(f"Minimum order ₹{coupon.minimum_amount}")

            # User specific coupon
            if coupon.users.exists():
                if not request.user.is_authenticated or request.user not in coupon.users.all():
                    raise Exception("Coupon not valid for you")

            # One time use
            if coupon.one_time_use and request.user.is_authenticated:
                if request.user in coupon.used_by.all():
                    raise Exception("Coupon already used")

            request.session['coupon_id'] = coupon.id
            request.session['coupon_error'] = None

        except Exception as e:
            request.session['coupon_error'] = str(e)
            request.session.pop('coupon_id', None)

    return redirect('cart')

def remove_coupon(request):
    request.session.pop('coupon_id', None)
    return redirect('cart')

@never_cache
def coupons_page(request):
    """Display all available coupons for user"""
    # Get cart to calculate current subtotal
    if request.user.is_authenticated:
        cart = get_or_create_user_cart(request.user)
    else:
        cart = get_or_create_session_cart(request)
    
    items = cart.items.all()
    subtotal = sum(item.quantity * item.product.price for item in items)
    
    # Get filter from request
    filter_type = request.GET.get('filter', 'all')
    
    # Get all available coupons with filter
    available_coupons = get_available_coupons(request, subtotal, filter_type)
    
    # Get currently applied coupon
    coupon = None
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id, active=True)
        except Coupon.DoesNotExist:
            request.session.pop('coupon_id', None)
    
    return render(request, "coupons.html", {
        "available_coupons": available_coupons,
        "applied_coupon": coupon,
        "subtotal": subtotal,
        "cart_count": items.count()
    })