from django.db import models
from django.contrib.auth.models import User  # <- Add this line
from django.urls import reverse


class Product(models.Model):

    CATEGORY_CHOICES = [
        ("water_tanks", "Water Tanks & Storage"),
        ("sanitation", "Sanitation"),
        ("agriculture", "Agriculture"),
        ("material_handling", "Material Handling"),
        ("water_supply", "Water Supply & Accessories"),
        ("special_products", "Special Products"),
    ]

    TYPE_CHOICES = [
        ("viable", "Viable"),
        ("simple", "Simple"),
    ]
    brochure = models.FileField(
        upload_to="brochures/",
        blank=True,
        null=True,
        help_text="Upload product brochure (PDF recommended)"
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to="products/")
    short_description = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="Brief summary shown on product cards or listings."
    )
    description = models.TextField(blank=True, null=True)
    stock_status = models.BooleanField(default=True)
    offers_delivery = models.BooleanField(
        default=False,
        help_text="Check this if this product requires delivery & shipping zone selection"
    )


    def get_category_url(self):
        mapping = {
            "water_tanks": "water_tank_storage",
            "sanitation": "sanitation",
            "agriculture": "agriculture",
            "material_handling": "material_handling",
            "water_supply": "water_supply_and_accessories",
            "special_products": "special_products_and_others",
        }
        return reverse(mapping[self.category])

    def __str__(self):
        return self.name

class ProductFeature(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="features",
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.product.name} - Feature"

class ProductApplication(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="applications",
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.product.name} - Application"

class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=200)  # e.g. "WASTE BIN 30"
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.name}"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    option = models.ForeignKey(ProductOption, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product', 'option')

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name='gallery_images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="products/gallery/")

    def __str__(self):
        return f"Image for {self.product.name}"

class Shipping(models.Model):
    label = models.CharField(max_length=50)
    details = models.TextField()

    def __str__(self):
        return self.label






