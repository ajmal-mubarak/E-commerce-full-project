from django.urls import path
from . import views

urlpatterns = [
    path('', views.wishlist_view, name='wishlist'),
    path('add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:item_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path("toggle/", views.toggle_wishlist_ajax, name="toggle_wishlist_ajax"),
    path('remove/product/<int:product_id>/',views.remove_from_wishlist_by_product,name='remove_from_wishlist_by_product'),

]
