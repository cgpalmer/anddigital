from django.db import models

# Create your models here.
class Enquiry(models.Model):
    enquiry = models.CharField(max_length=1000, null=False, blank=False)
    email = models.CharField(max_length=250, null=True, blank=True)
    tel = models.IntegerField(null=True, blank=True)
    

    def __str__(self):
        return self.enquiry

