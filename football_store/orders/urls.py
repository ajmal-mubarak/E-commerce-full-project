"""
URL configuration for football_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/buy-now/", views.checkout_buy_now, name="checkout_buy_now"),
    path("buy-now/<int:product_id>/", views.buy_now, name="buy_now"),
    path("success/<int:order_id>/", views.order_success, name="order_success"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("my-orders/filter/", views.filter_search_orders, name="filter_search_orders"),
    path("payment/simulated/<int:order_id>/", views.simulated_payment, name="simulated_payment"),
    path("payment/razorpay/<int:order_id>/", views.razorpay_payment, name="razorpay_payment"),
    path("payment/razorpay-callback/<int:order_id>/", views.razorpay_callback, name="razorpay_callback"),
    path("cancel/<int:order_id>/", views.cancel_order, name="cancel_order"),
]

