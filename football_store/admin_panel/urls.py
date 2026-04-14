from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),

    # Products
    path('products/', views.products_list, name='products_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/<int:pk>/images/add/', views.product_images_add, name='product_images_add'),

    # Categories
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # Orders
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/<int:pk>/status/', views.order_change_status, name='order_change_status'),

    # Users
    path('users/', views.users_list, name='users_list'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    
    # AJAX
    path('get-category-sizes/<int:category_id>/', views.get_category_sizes, name='get_category_sizes'),

    # Coupons
    path('coupons/', views.coupons_list, name='coupons_list'),
    path('coupons/add/', views.coupon_add, name='coupon_add'),
    path('coupons/<int:pk>/edit/', views.coupon_edit, name='coupon_edit'),
    path('coupons/<int:pk>/delete/', views.coupon_delete, name='coupon_delete'),

    # Bulk Delete
    path('products/bulk-delete/', views.products_bulk_delete, name='products_bulk_delete'),
    path('categories/bulk-delete/', views.categories_bulk_delete, name='categories_bulk_delete'),
    path('orders/bulk-delete/', views.orders_bulk_delete, name='orders_bulk_delete'),
    path('users/bulk-delete/', views.users_bulk_delete, name='users_bulk_delete'),
    path('coupons/bulk-delete/', views.coupons_bulk_delete, name='coupons_bulk_delete'),
]
