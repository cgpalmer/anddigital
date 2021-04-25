from django.shortcuts import render

# Create your views here.
def customer_enquiry(request):
    if form.is_valid():
        customer_enquiry = form.cleaned_data.get("enquiry")
        email = form.cleaned_data.get("email")
        tel = form.cleaned_data.get("tel")
        send_confirmation_email(self, customer_enquiry, email, tel)
    template = 'home/index.html'
    context = {        
    }

    return render(request, template, context)

def delivery_enquiry(request):
    
    template = 'home/index.html'
    context = {        
    }

    return render(request, template, context)


def send_confirmation_email(self, customer_enquiry, email, tel):
    cust_email = email
    """Send the user a confirmation email"""
    subject = render_to_string(
        'auto_query_response_subject.txt',
        )
    body = render_to_string(
        'customer_service/auto_response_to_query.txt',
        {'enquiry': customer_enquiry}
        )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )
