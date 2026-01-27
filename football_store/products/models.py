from django.db import models
from django.utils.text import slugify

CATEGORY_CHOICES = [
    ('boots', 'Football Boots'),
    ('jersey', 'Jersey'),
    ('shorts', 'Shorts'),
    ('socks', 'Socks'),
    ('other', 'Other'),
]

# Suggested predefined sizes
BOOT_SIZES = ['5', '6', '7', '8', '9']
JERSEY_SIZES = ['S', 'M', 'L', 'XL', 'XXL']
SHORTS_SIZES = ['Free Size']
SOCKS_SIZES = ['Free Size']

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    main_image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')

    is_featured = models.BooleanField(default=False)
    is_live = models.BooleanField(default=True)  # Soft delete
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        # Auto generate slug if empty
        if not self.slug:
            base_slug = slugify(self.name)[:200]
            slug = base_slug
            counter = 1

            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

        # Auto-create sizes based on category (only if sizes don't already exist)
        if self.category == 'boots' and self.sizes.count() == 0:
            for s in BOOT_SIZES:
                ProductSize.objects.create(product=self, size=s)
                
        if self.category == 'shorts' and self.sizes.count() == 0:
            for s in SHORTS_SIZES:
                ProductSize.objects.create(product=self, size=s)

        if self.category == 'socks' and self.sizes.count() == 0:
            for s in SOCKS_SIZES:
                ProductSize.objects.create(product=self, size=s)

        if self.category == 'jersey' and self.sizes.count() == 0:
            for s in JERSEY_SIZES:
                ProductSize.objects.create(product=self, size=s)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductSize(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    size = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.product.name} - {self.size}"
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

