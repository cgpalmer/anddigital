from django.db import models

# Create your models here.
class Enquiry(models.Model):
    enquiry = models.CharField(max_length=1000, null=False, blank=False)
    email = models.CharField(max_length=250, null=True, blank=True)
    tel = models.IntegerField(null=True, blank=True)
    

    def __str__(self):
        return self.enquiry

class Store(models.Model):
    store_name = models.CharField(max_length=100, null=False, blank=False)
    postcode = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.store_name

