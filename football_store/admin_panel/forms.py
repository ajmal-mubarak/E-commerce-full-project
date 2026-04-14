from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from products.models import Product, ProductImage, ProductSize, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image', 'sizes']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        self.fields['sizes'].widget.attrs.update({'placeholder': 'e.g., S,M,L,XL or 7,8,9,10', 'rows': 2})
from orders.models import Order
from django.utils.text import slugify


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'price', 'stock', 'description', 'main_image', 'category', 'is_featured', 'is_live']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in ['is_featured', 'is_live']:
                field.widget.attrs.update({'class': 'form-check-input'})
            elif name == 'main_image':
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        slug = cleaned_data.get("slug")

        if not slug and name:
            cleaned_data["slug"] = slugify(name)

        return cleaned_data


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class ProductSizeForm(forms.ModelForm):
    class Meta:
        model = ProductSize
        fields = ['size']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=3, can_delete=True, max_num=3)
ProductSizeFormSet = inlineformset_factory(Product, ProductSize, form=ProductSizeForm, extra=20, can_delete=True, max_num=20)

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']  # requires your Order model to have 'status' field (see note below)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active', 'is_staff']

from cart.models import Coupon

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount_type', 'discount_value', 'minimum_amount', 'active', 'expiry_date', 'users', 'one_time_use']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'users': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name in ['active', 'one_time_use']:
                field.widget.attrs.update({'class': 'form-check-input'})
            elif name == 'users':
                pass # Already handled in widgets
            else:
                field.widget.attrs.update({'class': 'form-control'})
