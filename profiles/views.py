from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import UserProfile
from django.contrib import messages
from .models import UserProfile
from products.models import Product
from .forms import UserProfileForm
from checkout.models import Order
from django.contrib.auth.decorators import login_required
import datetime




@login_required
def profile(request):
    """ Display the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')

    form = UserProfileForm(instance=profile)
    orders = profile.orders.all()
      

    template = 'profiles/profiles.html'
    context = {
        'current_user': profile,
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    
    }

    return render(request, template, context)


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    
    }

    return render(request, template, context)

