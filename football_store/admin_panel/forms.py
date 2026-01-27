from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from products.models import Product, ProductImage, ProductSize
from orders.models import Order
from django.utils.text import slugify


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'slug', 'price', 'description', 'main_image', 'category', 'is_featured', 'is_live']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


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

class ProductSizeForm(forms.ModelForm):
    class Meta:
        model = ProductSize
        fields = ['size']

ProductImageFormSet = inlineformset_factory(Product, ProductImage, form=ProductImageForm, extra=3, can_delete=True, max_num=10)
ProductSizeFormSet = inlineformset_factory(Product, ProductSize, form=ProductSizeForm, extra=1, can_delete=True, max_num=20)

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']  # requires your Order model to have 'status' field (see note below)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'is_staff']
