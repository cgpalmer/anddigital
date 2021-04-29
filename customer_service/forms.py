from django import forms
from .models import Enquiry

class EnquiryForm(forms.ModelForm):

    class Meta:
        enquiry = forms.CharField(widget=forms.Textarea)
        email = forms.EmailField()
        tel = forms.CharField(required=False)