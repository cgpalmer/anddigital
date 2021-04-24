from django import forms
from .models import Product


# This code was mainly taken from Boutique Ado - but has been modified to meet my project's needs.
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'