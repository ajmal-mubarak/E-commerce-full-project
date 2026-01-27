from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import reverse
from django.forms import modelform_factory
from django.db.models import Q

from products.models import Product
from orders.models import Order, OrderItem
from django.contrib.auth.models import User

from .forms import (
    ProductForm, ProductImageFormSet, ProductSizeFormSet,
    OrderStatusForm, UserForm
)

# Staff-only access rule
staff_required = user_passes_test(
    lambda u: u.is_active and u.is_staff,
    login_url='admin:login'
)


# ===================== DASHBOARD =====================
@staff_required
def dashboard_home(request):
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    recent_orders = Order.objects.order_by('-created_at')[:8]

    return render(request, 'admin_panel/dashboard_home.html', {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_users': total_users,
        'recent_orders': recent_orders,
    })


# ===================== PRODUCTS =====================
@staff_required
def products_list(request):
    query = request.GET.get("q", "")

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(slug__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'admin_panel/products_list.html', {
        'products': products,
        'search_query': query,
    })


@staff_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Product created!")
            return redirect('admin_panel:product_edit', pk=product.pk)
    else:
        form = ProductForm()

    return render(request, 'admin_panel/product_form.html', {
        'form': form,
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

    orders = Order.objects.all().order_by('-created_at')

    if query:
        orders = orders.filter(
            Q(id__icontains=query) |
            Q(user__username__icontains=query) |
            Q(phone__icontains=query) |
            Q(full_name__icontains=query)
        )

    return render(request, 'admin_panel/orders_list.html', {
        'orders': orders,
        'search_query': query
    })


@staff_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.items.all()
    return render(request, 'admin_panel/order_detail.html', {
        'order': order,
        'items': items
    })


@staff_required
def order_change_status(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Order status updated")
            return redirect('admin_panel:order_detail', pk=pk)

    else:
        form = OrderStatusForm(instance=order)

    return render(request, 'admin_panel/order_change_status.html', {
        'order': order,
        'form': form
    })


# ===================== USERS =====================
@staff_required
def users_list(request):
    query = request.GET.get("q", "")

    users = User.objects.all().order_by('-date_joined')

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query)
        )

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
