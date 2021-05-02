from django.db import models

# Create your models here.
from django.db import models
from django.db.models import CharField, Model
from django_mysql.models import ListCharField
from customer_service.models import Store
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=False, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    # category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    # this needs to be unique
    sku = models.CharField(max_length=254, null=False, blank=True)
    name = models.CharField(max_length=254, null=False, blank=False, default="new_product")
    friendly_name = models.CharField(max_length=254, null=False, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True)
    rating = models.IntegerField(default=0)
    number_of_ratings = models.IntegerField(null=True, blank=True, default=0)
    rating_total = models.IntegerField(null=True, blank=True, default=0)
    images = ListCharField(base_field=CharField(max_length=100),max_length=(6 * 110), null=True, blank=True)
    online_stock_count = models.IntegerField(default=0)
    store_stock_count = models.IntegerField(default=0)
    qr_status = models.BooleanField(default=False)
    qr_retrieval_key = models.CharField(max_length=254, default=str(uuid.uuid4()), null=False, blank=False)
    qr_code = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name


class Special(models.Model):
    name = models.CharField(max_length=254, null=True, blank=True, default="none")
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    discounts = models.DecimalField(max_digits=4, decimal_places=3, default=0.0, null=True, blank=False)

    def __str__(self):
        return self.name

class Product_stock(models.Model):
    store = models.ForeignKey('customer_service.Store', null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey('Product', null=True, blank=True, on_delete=models.SET_NULL)
    size = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(15)])
    stock_levels = models.IntegerField()

  
