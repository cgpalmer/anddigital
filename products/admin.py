from django.contrib import admin
from .models import Product, Category, Special


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'price',
        'rating',
        'image_mobile',
        'qr_code'
    )

    ordering = ('sku',)

admin.site.register(Product, ProductAdmin)