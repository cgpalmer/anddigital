from django import forms
from .models import Enquiry

class EnquiryForm(forms.ModelForm):

    class Meta:
        model = Enquiry
        fields = '__all__'
        widgets = {
            'enquiry': forms.Textarea(attrs={'rows': 4}),
        }

class DeliveryEnquiryForm(forms.Form): 
    delivery_enquiry = forms.CharField(max_length=50)