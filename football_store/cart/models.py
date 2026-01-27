from django.db import models
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Cart of {self.user.username}"
        return f"Session Cart {self.session_id}"

    @property
    def total(self):
        items = self.items.all()
        return sum(item.subtotal for item in items)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        if self.size:
            return f"{self.quantity} × {self.product.name} (Size: {self.size})"
        return f"{self.quantity} × {self.product.name}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity
    

class Coupon(models.Model):
    DISCOUNT_TYPE = (
        ('percent', 'Percentage'),
        ('amount', 'Fixed Amount'),
        ('free_shipping', 'Free Shipping'),
    )

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE)
    discount_value = models.PositiveIntegerField(default=0)

    minimum_amount = models.PositiveIntegerField(default=0)

    active = models.BooleanField(default=True)
    expiry_date = models.DateField(null=True, blank=True)

    users = models.ManyToManyField(
        User, blank=True,
        help_text="Leave empty for all users"
    )

    one_time_use = models.BooleanField(default=False)
    used_by = models.ManyToManyField(
        User, related_name="used_coupons", blank=True
    )

    def __str__(self):
        return self.code

