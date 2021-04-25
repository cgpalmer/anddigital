from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
import datetime

# Create your views here.
def customer_enquiry(request):
 
    customer_enquiry = request.POST.get("enquiry")
    print(customer_enquiry)
    email =  request.POST.get("email")
    tel =  request.POST.get("tel")
    send_query_confirmation_email(customer_enquiry, email, tel)
    send_store_query_email(customer_enquiry, email, tel)
    template = 'home/index.html'
    context = {        
    }

    return render(request, template, context)

def delivery_enquiry(request):
    
    template = 'home/index.html'
    context = {        
    }

    return render(request, template, context)

# https://github.com/lornebb/NullAnIon/blob/master/checkout/webhook_handler.py
def send_query_confirmation_email(customer_enquiry, email, tel):
    if email:
        cust_email = email
        """Send the user a confirmation email"""
        subject = render_to_string(
            'customer_service/auto_query_response_subject.txt',
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

def send_store_query_email(customer_enquiry, email, tel):
    cust_email = email
    cust_tel = tel
    store_email = 'cgpalmer91@gmail.com'
    enquiry_date = datetime.datetime.now()
    """Send the user a confirmation email"""
    subject = render_to_string(
        'customer_service/store_enquiry_subject.txt',
        {'enquiry_date': enquiry_date}
        )
    body = render_to_string(
        'customer_service/store_enquiry_body.txt',
        {'enquiry': customer_enquiry, 'cust_email': cust_email, 'cust_tel': tel}
        )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [store_email]
    )