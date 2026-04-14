from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.forms import modelform_factory
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
import datetime

from products.models import Product, Category
from orders.models import Order, OrderItem
from django.contrib.auth.models import User

from .forms import (
    ProductForm, ProductImageFormSet, ProductSizeFormSet,
    OrderStatusForm, UserForm, CategoryForm, CouponForm
)
from cart.models import Coupon

# Staff-only access rule
staff_required = user_passes_test(
    lambda u: u.is_active and u.is_staff,
    login_url='admin:login'
)

# ===================== CATEGORIES =====================
@staff_required
def categories_list(request):
    query = request.GET.get("q", "")
    categories = Category.objects.all().order_by('name')
    if query:
        categories = categories.filter(name__icontains=query)
    
    form = CategoryForm()
    return render(request, 'admin_panel/categories_list.html', {
        'categories': categories,
        'form': form,
        'search_query': query,
    })

@staff_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created!")
        else:
            messages.error(request, "Error creating category.")
    return redirect('admin_panel:categories_list')

@staff_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated!")
        else:
            messages.error(request, "Error updating category.")
    return redirect('admin_panel:categories_list')

@staff_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted.")
    return redirect('admin_panel:categories_list')



# ===================== DASHBOARD =====================
@staff_required
def dashboard_home(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    total_categories = Category.objects.count()
    total_coupons = Coupon.objects.count()
    recent_orders = Order.objects.order_by('-created_at')[:5]
    return render(request, 'admin_panel/dashboard_home.html', {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_categories': total_categories,
        'total_coupons': total_coupons,
        'recent_orders': recent_orders,
    })


# ===================== PRODUCTS =====================
@staff_required
def products_list(request):
    query = request.GET.get("q", "")
    
    # Filter params
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    products = Product.objects.all().order_by('-created_at')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(slug__icontains=query) |
            Q(description__icontains=query)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if date_from:
        products = products.filter(created_at__date__gte=date_from)
    if date_to:
        products = products.filter(created_at__date__lte=date_to)

    categories = Category.objects.all().order_by('name')

    return render(request, 'admin_panel/products_list.html', {
        'products': products,
        'search_query': query,
        'categories': categories,
    })


@staff_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        img_formset = ProductImageFormSet(request.POST, request.FILES)
        size_formset = ProductSizeFormSet(request.POST)
        
        if form.is_valid() and img_formset.is_valid() and size_formset.is_valid():
            product = form.save()
            
            # Save images
            img_formset.instance = product
            img_formset.save()
            
            # Save sizes
            size_formset.instance = product
            size_formset.save()
            
            messages.success(request, "Product created!")
            return redirect('admin_panel:products_list')
    else:
        form = ProductForm()
        img_formset = ProductImageFormSet()
        size_formset = ProductSizeFormSet()

    return render(request, 'admin_panel/product_form.html', {
        'form': form,
        'img_formset': img_formset,
        'size_formset': size_formset,
        'action': 'Add',
    })

# ----------------- ADD PRODUCT IMAGES -----------------
@staff_required
def product_images_add(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        img_formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        
        if img_formset.is_valid():
            img_formset.save()
            messages.success(request, "Images updated successfully.")
            return redirect('admin_panel:product_edit', pk=pk)

    else:
        img_formset = ProductImageFormSet(instance=product)

    return render(request, 'admin_panel/product_images.html', {
        'img_formset': img_formset,
        'product': product,
    })


@staff_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        img_formset = ProductImageFormSet(request.POST, request.FILES, instance=product)
        size_formset = ProductSizeFormSet(request.POST, instance=product)

        if form.is_valid() and img_formset.is_valid() and size_formset.is_valid():
            form.save()
            img_formset.save()
            size_formset.save()
            messages.success(request, "Product updated!")
            return redirect('admin_panel:products_list')

    else:
        form = ProductForm(instance=product)
        img_formset = ProductImageFormSet(instance=product)
        size_formset = ProductSizeFormSet(instance=product)

    return render(request, 'admin_panel/product_form.html', {
        'form': form,
        'img_formset': img_formset,
        'size_formset': size_formset,
        'product': product,
        'action': 'Edit',
    })


@staff_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect('admin_panel:products_list')

    return render(request, 'admin_panel/product_confirm_delete.html', {
        'product': product
    })


# ===================== ORDERS =====================
@staff_required
def orders_list(request):
    query = request.GET.get("q", "")
    
    # Filters
    status = request.GET.get('status')
    min_total = request.GET.get('min_total')
    max_total = request.GET.get('max_total')
    date_range_preset = request.GET.get('date_range_preset')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    orders = Order.objects.all().order_by('-created_at')

    if query:
        orders = orders.filter(
            Q(id__icontains=query) |
            Q(user__username__icontains=query) |
            Q(phone__icontains=query) |
            Q(full_name__icontains=query)
        )
    
    if status:
        orders = orders.filter(status=status)
    if min_total:
        orders = orders.filter(total_amount__gte=min_total)
    if max_total:
        orders = orders.filter(total_amount__lte=max_total)

    # Date Logic
    today = timezone.now().date()
    if date_range_preset == '7d':
        orders = orders.filter(created_at__date__gte=today - timedelta(days=7))
    elif date_range_preset == '30d':
        orders = orders.filter(created_at__date__gte=today - timedelta(days=30))
    elif date_range_preset == '365d':
        orders = orders.filter(created_at__date__gte=today - timedelta(days=365))
    elif date_range_preset == 'this_month':
        orders = orders.filter(created_at__year=today.year, created_at__month=today.month)
    elif date_range_preset == 'this_year':
        orders = orders.filter(created_at__year=today.year)
    elif date_range_preset == 'custom':
        if date_from:
            orders = orders.filter(created_at__date__gte=date_from)
        if date_to:
            orders = orders.filter(created_at__date__lte=date_to)

    return render(request, 'admin_panel/orders_list.html', {
        'orders': orders,
        'search_query': query
    })




@staff_required
def order_change_status(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Order #{order.id} status updated to {order.get_status_display()}")
        else:
            messages.error(request, "Error updating order status.")
    
    return redirect('admin_panel:orders_list')


# ===================== USERS =====================
@staff_required
def users_list(request):
    query = request.GET.get("q", "")
    
    role = request.GET.get('role')
    status = request.GET.get('status')

    users = User.objects.all().order_by('-date_joined')

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )
    
    if role == 'staff':
        users = users.filter(is_staff=True)
    elif role == 'user':
        users = users.filter(is_staff=False)
        
    if status == 'active':
        users = users.filter(is_active=True)
    elif status == 'inactive':
        users = users.filter(is_active=False)

    return render(request, 'admin_panel/users_list.html', {
        'users': users,
        'search_query': query
    })


@staff_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated.")
            return redirect('admin_panel:users_list')
    else:
        form = UserForm(instance=user)

    return render(request, 'admin_panel/user_form.html', {
        'form': form,
        'user_obj': user
    })


@staff_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        user.delete()
        messages.success(request, "User removed.")
        return redirect('admin_panel:users_list')

    return render(request, 'admin_panel/user_confirm_delete.html', {
        'user_obj': user
    })


# ===================== AJAX ENDPOINTS =====================
@staff_required
def get_category_sizes(request, category_id):
    """AJAX endpoint to get sizes for a category"""
    try:
        category = get_object_or_404(Category, pk=category_id)
        sizes = category.get_sizes_list()
        return JsonResponse({'sizes': sizes})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ===================== COUPONS =====================
@staff_required
def coupons_list(request):
    query = request.GET.get("q", "")
    
    active_filter = request.GET.get('active')
    min_val = request.GET.get('min_val')
    max_val = request.GET.get('max_val')
    exp_from = request.GET.get('exp_from')
    exp_to = request.GET.get('exp_to')

    coupons = Coupon.objects.all().order_by('-id')
    
    if query:
        coupons = coupons.filter(code__icontains=query)
    
    if active_filter == 'yes':
        coupons = coupons.filter(active=True)
    elif active_filter == 'no':
        coupons = coupons.filter(active=False)
        
    if min_val:
        coupons = coupons.filter(discount_value__gte=min_val)
    if max_val:
        coupons = coupons.filter(discount_value__lte=max_val)
        
    if exp_from:
        coupons = coupons.filter(expiry_date__gte=exp_from)
    if exp_to:
        coupons = coupons.filter(expiry_date__lte=exp_to)

    form = CouponForm()
    all_users = User.objects.all()
    
    return render(request, 'admin_panel/coupons_list.html', {
        'coupons': coupons,
        'form': form,
        'all_users': all_users,
        'search_query': query
    })

@staff_required
def coupon_add(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon created successfully!")
        else:
            messages.error(request, f"Error creating coupon: {form.errors}")
    return redirect('admin_panel:coupons_list')

@staff_required
def coupon_edit(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, "Coupon updated successfully!")
        else:
            messages.error(request, "Error updating coupon.")
    return redirect('admin_panel:coupons_list')

@staff_required
def coupon_delete(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        coupon.delete()
        messages.success(request, "Coupon deleted.")
    return redirect('admin_panel:coupons_list')

# ===================== BULK ACTIONS =====================
@staff_required
def products_bulk_delete(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        if selected_ids:
            Product.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f"{len(selected_ids)} products deleted.")
        else:
            messages.warning(request, "No products selected.")
    return redirect('admin_panel:products_list')

@staff_required
def categories_bulk_delete(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        if selected_ids:
            Category.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f"{len(selected_ids)} categories deleted.")
        else:
            messages.warning(request, "No categories selected.")
    return redirect('admin_panel:categories_list')

@staff_required
def orders_bulk_delete(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        if selected_ids:
            Order.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f"{len(selected_ids)} orders deleted.")
        else:
            messages.warning(request, "No orders selected.")
    return redirect('admin_panel:orders_list')

@staff_required
def users_bulk_delete(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        if selected_ids:
            User.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f"{len(selected_ids)} users deleted.")
        else:
            messages.warning(request, "No users selected.")
    return redirect('admin_panel:users_list')

@staff_required
def coupons_bulk_delete(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        if selected_ids:
            Coupon.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f"{len(selected_ids)} coupons deleted.")
        else:
            messages.warning(request, "No coupons selected.")
    return redirect('admin_panel:coupons_list')

