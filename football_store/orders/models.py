from django.db import models
from django.contrib.auth.models import User
from cart.models import Coupon
from products.models import Product

# -----------------------------
# ORDER STATUS (Delivery)
# -----------------------------
STATUS_CHOICES = [
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
    ("cancelled", "Cancelled"),
]

# -----------------------------
# PAYMENT STATUS (Online)
# -----------------------------
PAYMENT_STATUS_CHOICES = (
    ("PENDING", "Pending"),
    ("PAID", "Paid"),
    ("FAILED", "Failed"),
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Payment
    payment_method = models.CharField(
        max_length=20,
        default="COD"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="PENDING"
    )

    # Order lifecycle
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="processing"
    )

    # Coupon details
    subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    shipped_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
    
    def get_expected_delivery_date(self):
        """Calculate expected delivery date (7 days from order creation)"""
        from datetime import timedelta
        return self.created_at + timedelta(days=7)


class OrderStatusHistory(models.Model):
    """Track order status changes with timestamps"""
    order = models.ForeignKey(Order, related_name="status_history", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['changed_at']
        verbose_name_plural = "Order Status Histories"
    
    def __str__(self):
        return f"Order #{self.order.id} - {self.status} at {self.changed_at}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=20, null=True, blank=True)

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        if self.size:
            return f"{self.order.id} - {self.product.name} (Size: {self.size})"
        return f"{self.order.id} - {self.product.name}"


# -----------------------------
# USER ADDRESS
# -----------------------------
ADDRESS_TYPE = (
    ('home', 'Home'),
    ('work', 'Work'),
)

class UserAddress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )

    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    address_type = models.CharField(
        max_length=10,
        choices=ADDRESS_TYPE
    )

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'address_type')

    def __str__(self):
        return f"{self.user.username} - {self.address_type}"
