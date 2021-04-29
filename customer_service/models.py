from django.db import models

# Create your models here.
class Enquiry(models.Model):
    # category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    # this needs to be unique
    enquiry = models.CharField(max_length=1000, null=False, blank=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    tel = models.IntegerField(null=True, blank=True)
    

    def __str__(self):
        return self.enquiry