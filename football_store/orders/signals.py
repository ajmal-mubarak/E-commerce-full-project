from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order, OrderStatusHistory


@receiver(pre_save, sender=Order)
def track_order_status_change(sender, instance, **kwargs):
    """Track when order status changes"""
    if instance.pk:  # Only if the order already exists (update, not create)
        try:
            old_order = Order.objects.get(pk=instance.pk)
            if old_order.status != instance.status:
                instance._status_changed = True
                instance._old_status = old_order.status
        except Order.DoesNotExist:
            pass


@receiver(post_save, sender=Order)
def create_order_status_history(sender, instance, created, **kwargs):
    """Create OrderStatusHistory entry when order is created or status changes"""
    if created:
        # Create initial status entry
        OrderStatusHistory.objects.create(
            order=instance,
            status=instance.status
        )
    elif hasattr(instance, '_status_changed') and instance._status_changed:
        # Create entry for status change
        OrderStatusHistory.objects.create(
            order=instance,
            status=instance.status
        )
