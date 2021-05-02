from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product, Product_stock
from customer_service.models import Store
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
from basket.context import basket_contents
from basket.views import emptyingBasket
import stripe
import json


# This function has been copied directly from Boutique Ado - Code Institute
@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'basket': json.dumps(request.session.get('minified_basket', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


''' This function checks to see if the user has created duplicate
    items whilst editing the basket. It the removes the duplicates
    and updates the quantity.
'''


def condensing_basket(request):
    basket = request.session.get('basket', {})
    if basket != {}:
            # Looping through the basket to form a list of items to check.
        for item in basket['items']:

            appending_item = [item['basket_item_id'], int(item['quantity']), [item['item_id'], item['size'],]]
            list_of_items_to_check.append(appending_item)

        # Finding the initial duplications
        for i in range(0, len(list_of_items_to_check)):
            for j in range(i+1, len(list_of_items_to_check)):
                if list_of_items_to_check[i][2] == list_of_items_to_check[j][2]:
                    duplicates_found.append([list_of_items_to_check[i], list_of_items_to_check[j]])

        # Updating the quantity of the duplicates
        for k in range(len(duplicates_found)):
            for item in basket['items']:
                if item['digital_download'] is None:
                    if item['basket_item_id'] == duplicates_found[k][0][0]:
                        item['quantity'] = item['quantity'] + duplicates_found[k][1][1]
                        request.session['basket'] = basket

        # Deleting a duplicate
        for k in range(len(duplicates_found)):
            item_number = -1
            for item in basket['items']:
                item_number = item_number + 1
                if item['basket_item_id'] == duplicates_found[k][1][0]:
                    del basket['items'][item_number]
                request.session['basket'] = basket
        return redirect(checkout)
    else:
        messages.error(request, 'It looks like your basket is empty. Please add some items to continue.')
        return redirect('view_basket')


'''
This majority of this function has been copied directly from
Boutique Ado - Code Institute, with minor adjustments from me.
'''


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        basket = request.session.get('basket', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }
        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket['items'])
            order.save()

            # This checks the delivery method.
            for item in basket['items']:
                try:
                    product = get_object_or_404(Product, pk=item['item_id'])

                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item["quantity"],
                        
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your basket wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_basket'))

            request.session['save_info'] = 'save-info' in request.POST
            removing_stock(request)
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "There's nothing in your basket at the moment")
            return redirect(reverse('products'))

        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.user.get_full_name(),
                    'email': profile.user.email,
                    'phone_number': profile.default_phone_number,
                    'country': profile.default_country,
                    'postcode': profile.default_postcode,
                    'town_or_city': profile.default_town_or_city,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'county': profile.default_county,
                    })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    # This is where orders are stored for digital downloads.
    basket = request.session.get('basket', {})
    if basket != {}:
        for item in basket['items']:
            product = get_object_or_404(Product, pk=item['item_id'])
            sku = product.sku
            name = product.friendly_name
            

    emptyingBasket(request)

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
      
    }

    return render(request, template, context)

def removing_stock(request):
    basket = request.session.get('basket', {})
    store = get_object_or_404(Store, store_name="Online")
    for item in basket['items']:
        product = get_object_or_404(Product, pk=item['item_id'])
        product_stock = get_object_or_404(Product_stock, product=item['item_id'], size=item['size'], store=store)
        product_stock.stock_levels = product_stock.stock_levels - item['quantity']
        product.online_stock_count = product.online_stock_count - item['quantity']
        product.save()
        product_stock.save()
    return 
    