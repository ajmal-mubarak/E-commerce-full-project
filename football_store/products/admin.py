from django.contrib import admin
from .models import Product, ProductImage, ProductSize, Category

# -------------------------
# CATEGORY ADMIN
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sizes")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    fieldsets = (
        ('Category Information', {
            'fields': ('name', 'slug', 'image')
        }),
        ('Sizes', {
            'fields': ('sizes',),
            'description': 'Enter sizes separated by commas (e.g., S,M,L,XL or 5,6,7,8,9 or Free Size)'
        }),
    )


# -------------------------
# INLINE MODELS
# -------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 2
    fields = ["image"]


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    fields = ["size"]
    readonly_fields = []


# -------------------------
# PRODUCT ADMIN
# -------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name", 
        "category", 
        "price", 
        "is_featured", 
        "is_live", 
        "created_at",
        "stock",
        "get_sizes_display"
    )
    list_filter = ("is_featured", "is_live", "category")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("-created_at",)

    inlines = [ProductImageInline, ProductSizeInline]
    
    def get_sizes_display(self, obj):
        """Display available sizes for the product"""
        sizes = obj.sizes.all().values_list('size', flat=True)
        if sizes:
            return ", ".join(sizes)
        return "No sizes"
    
    get_sizes_display.short_description = "Available Sizes"


# -------------------------
# EXTRA ADMIN REGISTRATION
# -------------------------
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "image")


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ("product", "size")
