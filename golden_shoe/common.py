from customer_service.forms import EnquiryForm, DeliveryEnquiryForm

def context(request):
    context = {
        'enquiry': EnquiryForm,
        'delivery_enquiry': DeliveryEnquiryForm,
    }
    return context