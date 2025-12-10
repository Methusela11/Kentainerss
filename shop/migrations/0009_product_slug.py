from django.db import migrations, models
from django.utils.text import slugify


def generate_unique_slugs(apps, schema_editor):
    Product = apps.get_model("shop", "Product")

    for product in Product.objects.all():
        base_slug = slugify(product.name)
        slug = base_slug
        counter = 1

        # Ensure slug is unique
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        product.slug = slug
        product.save()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_product_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True, blank=True, null=True),
        ),
        migrations.RunPython(generate_unique_slugs),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
