from django.contrib import admin
from .models import Order, OrderItem, OrderStatusHistory

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'size')
    fields = ('product', 'quantity', 'price', 'size')

class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ('status', 'changed_at')
    fields = ('status', 'changed_at')
    can_delete = False

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'full_name', 'phone', 'status',
        'total_amount','subtotal_amount','coupon','discount_amount', 'created_at', 'shipped_date', 'show_items', 'show_quantities', 'show_sizes'
    )

    list_filter = ("status", "created_at")
    search_fields = ("id", "user__username", "full_name")
    inlines = [OrderItemInline, OrderStatusHistoryInline]

    list_editable = ('status', 'shipped_date')

    def show_items(self, obj):
        return ", ".join([item.product.name for item in obj.items.all()])
    show_items.short_description = "Items"

    def show_quantities(self, obj):
        return ", ".join([str(item.quantity) for item in obj.items.all()])
    show_quantities.short_description = "Quantities"
    
    def show_sizes(self, obj):
        sizes = [item.size if item.size else "—" for item in obj.items.all()]
        return ", ".join(sizes)
    show_sizes.short_description = "Sizes"

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(OrderStatusHistory)
