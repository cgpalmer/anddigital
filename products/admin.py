from django.contrib import admin
from .models import Product, Category, Special, Product_stock


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'price',
        'rating',
        'images',
        'qr_code'
    )

    ordering = ('sku',)

class Product_stockAdmin(admin.ModelAdmin):
    list_display = (
            'store',
            'product',
        )

admin.site.register(Product, ProductAdmin)
admin.site.register(Product_stock, Product_stockAdmin)