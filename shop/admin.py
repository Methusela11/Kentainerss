from django.contrib import admin
from .models import Product, CartItem, ProductOption, ProductImage, ProductApplication, ProductFeature

admin.site.register(Product)

admin.site.register(CartItem)

admin.site.register(ProductOption)

admin.site.register(ProductImage)

admin.site.register(ProductApplication)

admin.site.register(ProductFeature)

class ProductImageInline(admin.TabularInline):  # or StackedInline for big previews
    model = ProductImage
    extra = 1

