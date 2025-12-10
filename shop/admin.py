from django.contrib import admin
from .models import Product, CartItem, ProductOption, ProductImage

admin.site.register(Product)

admin.site.register(CartItem)

admin.site.register(ProductOption)

admin.site.register(ProductImage)

class ProductImageInline(admin.TabularInline):  # or StackedInline for big previews
    model = ProductImage
    extra = 1

