from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from cart.utils import get_or_create_user_cart
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
from django.db.models import Q
from cart.models import Coupon
from products.models import Product
from django.db import transaction
from django.contrib import messages
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .models import Order, OrderItem, UserAddress


# ---------------------------------
# NORMAL CHECKOUT (CART)
# ---------------------------------
@login_required
@never_cache
def checkout(request):
    cart = get_or_create_user_cart(request.user)
    cart_items = cart.items.all()

    subtotal = sum(item.product.price * item.quantity for item in cart_items)

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
            pass

    # Shipping fee logic
    shipping_fee = 12
    if coupon and coupon.discount_type == 'free_shipping':
        shipping_fee = 0

    total = max(subtotal - discount + shipping_fee, 0)

    addresses = UserAddress.objects.filter(user=request.user)

    if request.method == "POST":
        address_choice = request.POST.get("address_choice")

        # ----------------------------
        # NEW ADDRESS
        # ----------------------------
        if address_choice == "new" or not addresses.exists():
            full_name = request.POST.get("full_name")
            phone = request.POST.get("phone")
            address = request.POST.get("address")
            city = request.POST.get("city")
            pincode = request.POST.get("pincode")

            # Save as HOME if no addresses
            if not addresses.exists():
                UserAddress.objects.create(
                    user=request.user,
                    address_type="home",
                    full_name=full_name,
                    phone=phone,
                    address=address,
                    city=city,
                    pincode=pincode,
                    is_default=True
                )

        # ----------------------------
        # EXISTING ADDRESS
        # ----------------------------
        else:
            selected_address = get_object_or_404(
                UserAddress,
                id=address_choice,
                user=request.user
            )
            full_name = selected_address.full_name
            phone = selected_address.phone
            address = selected_address.address
            city = selected_address.city
            pincode = selected_address.pincode

        payment_method = request.POST.get("payment_method", "COD")

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    full_name=full_name,
                    phone=phone,
                    address=address,
                    city=city,
                    pincode=pincode,
                    subtotal_amount=subtotal,
                    discount_amount=discount,
                    total_amount=total,
                    coupon=coupon,
                    payment_method=payment_method,
                    payment_status="PENDING"
                )

                for item in cart_items:
                    # Lock the product row to prevent race conditions
                    product = Product.objects.select_for_update().get(id=item.product.id)
                    
                    if product.stock < item.quantity:
                        raise Exception(f"Not enough stock for {product.name}. Available: {product.stock}")
                    
                    product.stock -= item.quantity
                    product.save()

                    OrderItem.objects.create(
                        order=order,
                        product=product,  # Use the locked product instance
                        quantity=item.quantity,
                        price=product.price,
                        size=item.size,
                    )

                cart.items.all().delete()
                request.session.pop('coupon_id', None)

        except Exception as e:
            messages.error(request, str(e))
            return redirect("cart")

        if order.payment_method == "RAZORPAY":
            return redirect("razorpay_payment", order_id=order.id)
        elif order.payment_method == "SIMULATED":
            return redirect("simulated_payment", order_id=order.id)
        else:
            return redirect("order_success", order_id=order.id)

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "discount": discount,
        "coupon": coupon,
        "total": total,
        "shipping_fee": shipping_fee,
        "addresses": addresses,
    })


# ---------------------------------
# BUY NOW
# ---------------------------------
@login_required
@never_cache
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get("quantity", 1))
    size = request.POST.get("size", "").strip()

    # Size is required for all products
    if not size:
        return redirect("product_details", slug=product.slug)

    request.session["buy_now"] = {
        "product_id": product.id,
        "quantity": quantity,
        "size": size
    }

    return redirect("checkout_buy_now")


@login_required
@never_cache
def checkout_buy_now(request):
    data = request.session.get("buy_now")
    if not data:
        return redirect("products")

    product = get_object_or_404(Product, id=data["product_id"])
    qty = int(request.GET.get("quantity", data["quantity"]))
    size = data.get("size")
    size = data.get("size")
    subtotal = product.price * qty
    shipping_fee = 12
    total = subtotal + shipping_fee

    # Redirect if size is missing (size is always required)
    if not size:
        return redirect("product_details", slug=product.slug)

    addresses = UserAddress.objects.filter(user=request.user)

    if request.method == "POST":
        address_choice = request.POST.get("address_choice")

        if address_choice == "new" or not addresses.exists():
            full_name = request.POST.get("full_name")
            phone = request.POST.get("phone")
            address = request.POST.get("address")
            city = request.POST.get("city")
            pincode = request.POST.get("pincode")

            if not addresses.exists():
                UserAddress.objects.create(
                    user=request.user,
                    address_type="home",
                    full_name=full_name,
                    phone=phone,
                    address=address,
                    city=city,
                    pincode=pincode,
                    is_default=True
                )
        else:
            selected_address = get_object_or_404(
                UserAddress,
                id=address_choice,
                user=request.user
            )
            full_name = selected_address.full_name
            phone = selected_address.phone
            address = selected_address.address
            city = selected_address.city
            pincode = selected_address.pincode

        payment_method = request.POST.get("payment_method", "COD")

        try:
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    full_name=full_name,
                    phone=phone,
                    address=address,
                    city=city,
                    pincode=pincode,
                    total_amount=total,
                    payment_method=payment_method,
                    payment_status="PENDING"
                )

                # Lock the product
                locked_product = Product.objects.select_for_update().get(id=product.id)

                if locked_product.stock < qty:
                    raise Exception(f"Not enough stock for {locked_product.name}. Available: {locked_product.stock}")

                locked_product.stock -= qty
                locked_product.save()

                OrderItem.objects.create(
                    order=order,
                    product=locked_product,
                    quantity=qty,
                    price=locked_product.price,
                    size=size,
                )
        except Exception as e:
            messages.error(request, str(e))
            return redirect("product_details", slug=product.slug)

        del request.session["buy_now"]

        if order.payment_method == "RAZORPAY":
            return redirect("razorpay_payment", order_id=order.id)
        elif order.payment_method == "SIMULATED":
            return redirect("simulated_payment", order_id=order.id)
        else:
            return redirect("order_success", order_id=order.id)

    return render(request, "checkout_buy_now.html", {
        "product": product,
        "quantity": qty,
        "subtotal": subtotal,
        "shipping_fee": shipping_fee,
        "total": total,
        "addresses": addresses,
        "buy_size": size,
    })


# ---------------------------------
# SIMULATED PAYMENT
# ---------------------------------
@login_required
@never_cache
def simulated_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.payment_status != "PENDING":
        return redirect("order_success", order_id=order.id)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "success":
            order.payment_status = "PAID"
            order.save()
            return redirect("order_success", order_id=order.id)

        elif action == "fail":
            order.payment_status = "FAILED"
            order.status = "cancelled"
            order.save()
            return redirect("my_orders")

    return render(request, "payments/simulated_payment.html", {
        "order": order
    })


# ---------------------------------
# ORDER SUCCESS
# ---------------------------------
@login_required
@never_cache
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order_success.html", {"order": order})


# ---------------------------------
# MY ORDERS
# ---------------------------------
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-id")
    return render(request, "my_orders.html", {"orders": orders})


# ---------------------------------
# FILTER AND SEARCH API
# ---------------------------------
@login_required
@require_http_methods(["GET"])
def filter_search_orders(request):
    """API endpoint for filtering and searching orders"""
    try:
        orders = Order.objects.filter(user=request.user).order_by("-id")
        
        # Get filter parameters
        status_filters = request.GET.getlist('status')
        time_filters = request.GET.getlist('time')
        search_query = request.GET.get('search', '').strip()
        
        # Apply status filters
        if status_filters:
            orders = orders.filter(status__in=status_filters)
        
        # Apply time filters - build a Q object for OR conditions between time options
        if time_filters:
            today = datetime.now()
            time_query = Q()
            
            if '30days' in time_filters:
                thirty_days_ago = today - timedelta(days=30)
                time_query |= Q(created_at__gte=thirty_days_ago)
            
            if '2024' in time_filters:
                time_query |= Q(created_at__year=2024)
            
            if '2023' in time_filters:
                time_query |= Q(created_at__year=2023)
            
            if 'older' in time_filters:
                # Older than 2023
                time_query |= Q(created_at__year__lt=2023)
            
            if time_query:
                # This time_query is combined with AND to the existing filters
                orders = orders.filter(time_query)
        
        # Apply search filter
        if search_query:
            orders = orders.filter(
                Q(full_name__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(id__icontains=search_query) |
                Q(items__product__name__icontains=search_query)
            ).distinct()
        
        # Build response with order cards HTML
        orders_html = ""
        
        if orders.exists():
            for order in orders:
                first_item = order.items.all().first()
                
                if first_item:
                    # Safely get image URL
                    img_src = first_item.product.main_image.url if first_item.product.main_image else ""
                    product_name = first_item.product.name
                    product_slug = first_item.product.slug
                    product_details_url = f"/products/{product_slug}/"
                    size = first_item.size or ""
                    # Category is now a ForeignKey, get the category name
                    category_display = first_item.product.category.name if first_item.product.category else ""
                else:
                    img_src = ""
                    product_name = "N/A"
                    product_slug = ""
                    product_details_url = "#"
                    size = ""
                    category_display = ""
                
                status_display = order.get_status_display() if hasattr(order, 'get_status_display') else order.status
                created_date = order.created_at.strftime("%b %d, %Y")
                expected_delivery_date = order.get_expected_delivery_date().strftime("%b %d, %Y")
                order_date = order.created_at.strftime("%Y-%m-%d")
                
                img_html = f'<img src="{img_src}" alt="{product_name}" class="product-img">' if img_src else '<div class="product-img"></div>'
                
                size_html = f'Size: {size}<br>' if size else ''
                category_html = f'Category: {category_display}' if category_display else ''
                
                view_details_btn = f'<a href="/orders/{order.id}/" class="action-link details-link"><i class="fa fa-eye"></i> View Details</a>' if order.status == 'delivered' else ''
                
                orders_html += f'''
                <div class="order-card" data-order-status="{order.status}" data-order-date="{order_date}">
                    <div class="order-card-header">
                        <div class="order-product-image">
                            {img_html}
                            <a href="#" class="back-arrow">
                                <i class="fa fa-chevron-left"></i>
                            </a>
                        </div>
                        
                        <div class="order-info-left">
                            <h3 class="product-name">
                                <a href="{product_details_url}">
                                    {product_name[:50]}
                                </a>
                            </h3>
                            
                            <p class="product-details">
                                {size_html}
                                {category_html}
                            </p>
                            
                            <p class="order-price">₹{order.total_amount}</p>
                        </div>
                    </div>
                    
                    <div class="order-status-section">
                        <div class="status-badge" data-status="{order.status}">
                            <span class="status-dot {order.status}"></span>
                            {status_display}
                        </div>
                        <span class="order-date">Expected by {expected_delivery_date}</span>
                    </div>
                    
                    <div class="order-actions">
                        {view_details_btn}
                    </div>
                </div>
                '''
        else:
            orders_html = '''
            <div class="empty-orders">
                <i class="fa fa-inbox"></i>
                <h3>No Orders Found</h3>
                <p>Try adjusting your filters or search terms.</p>
            </div>
            '''
        
        return JsonResponse({
            'success': True,
            'html': orders_html,
            'count': orders.count()
        })
    
    except Exception as e:
        import traceback
        error_msg = traceback.format_exc()
        print(f"Error in filter_search_orders: {error_msg}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ---------------------------------
# CANCEL ORDER
# ---------------------------------
@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'processing':
        order.status = 'cancelled'
        order.save()
        # You might want to add logic here to refund if payment was already made (e.g., wallet/stripe)
        # For now, just status update as per request.
        
    return redirect('my_orders')


# ---------------------------------
# RAZORPAY PAYMENT
# ---------------------------------
@login_required
@never_cache
def razorpay_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.payment_status != "PENDING":
        return redirect("order_success", order_id=order.id)
        
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    amount_in_paise = int(order.total_amount * 100)
    
    razorpay_order = client.order.create({
        "amount": amount_in_paise,
        "currency": "INR",
        "payment_capture": "1"
    })
    
    context = {
        "order": order,
        "razorpay_order_id": razorpay_order['id'],
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "amount": order.total_amount,
        "amount_in_paise": amount_in_paise,
    }
    
    return render(request, "payments/razorpay_payment.html", context)


from django.http import HttpResponse

@csrf_exempt
def razorpay_callback(request, order_id=None):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            
            if not order_id:
                order_id = request.POST.get('order_id', '')
            
            if not order_id:
                return HttpResponse("Order ID missing in callback data", status=400)
                
            try:
                order = Order.objects.get(id=int(order_id))
            except (Order.DoesNotExist, ValueError):
                return HttpResponse("Order not found or invalid ID", status=404)
                
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            client.utility.verify_payment_signature(params_dict)
            
            # Payment Successful
            order.payment_status = "PAID"
            order.status = "processing"
            order.save()
            return redirect('order_success', order_id=order.id)
            
        except razorpay.errors.SignatureVerificationError:
            # Payment Failed
            if 'order' in locals():
                order.payment_status = "FAILED"
                order.status = "cancelled"
                order.save()
            messages.error(request, "Payment signature verification failed.")
            return redirect('my_orders')
            
        except Exception as e:
            # Any other error
            import traceback
            error_details = traceback.format_exc()
            print("Razorpay Callback Error: ", error_details)
            return HttpResponse(f"An unexpected error occurred during payment verification: {str(e)}", status=500)
            
    return redirect('my_orders')

