from django.shortcuts import render

# Create your views here.
def customer_enquiry(request):
    
    template = 'home/index.html'
    context = {        
    }

    return render(request, template, context)

def delivery_enquiry(request):
    
    template = 'home/index.html'
    context = {        
    }

    return render(request, template, context)


def send_confirmation_email(self, order):
    cust_email = order.email
    """Send the user a confirmation email"""
    subject = render_to_string(
        'checkout/confirmation_emails/confirmation_email_subject.txt',
        {'order': order})
    body = render_to_string(
        'checkout/confirmation_emails/confirmation_email_body.txt',
        {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [cust_email]
    )
