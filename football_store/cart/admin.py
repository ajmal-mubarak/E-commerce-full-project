from django.contrib import admin
from .models import Coupon

# Register your models here.

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'discount_type', 'discount_value',
        'minimum_amount', 'active', 'expiry_date'
    )
    list_filter = ('active', 'discount_type')
    search_fields = ('code',)
    filter_horizontal = ('users', 'used_by')
