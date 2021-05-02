from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product



# This code was initially copied from Boutique Ado but has been changed to suit my website.
def basket_contents(request):

    basket_items = []
    minified_items = []
    total = 0
    full_price_total = 0
    products = None
  
    product_count = 0
    delivery_total = 0
    basket = request.session.get('basket', {})

    if basket != {}:
        for item in basket['items']:
            product_count += 1
            product = get_object_or_404(Product, pk=item['item_id'])
            subtotal = product.price * item['quantity']
            # size = item['size']
            full_price_sub_total = product.price * item['quantity']
            item_image = product.images[0]
            print(item_image)
            # Check delivery method
           
            delivery_total += subtotal

            total += subtotal
            full_price_total += full_price_sub_total

            basket_items.append({
                'item': item,
                'item_image': item_image,
                'product': product,
                'subtotal': subtotal,
                # 'size':size
     
            })

            minified_items.append({
                'product_id': product.id,
                'quantity': item['quantity'],
                'subtotal': subtotal,
                # 'size':size

            })

         

    # Calculate if eligble for free delivery
    if delivery_total == 0 or total > settings.FREE_DELIVERY_AMOUNT:
        delivery = 0
        free_delivery_deficit = 0
    else:
        delivery = Decimal.from_float(settings.STANDARD_DELIVERY_AMOUNT)
        free_delivery_deficit = settings.FREE_DELIVERY_AMOUNT - delivery_total

    money_saved = full_price_total - total
    grand_total = delivery + total
    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_deficit': free_delivery_deficit,
        'FREE_DELIVERY_AMOUNT': settings.FREE_DELIVERY_AMOUNT,
        'grand_total': grand_total,
        'delivery_total': delivery_total,
       
        'products': products,
   
        'minified_items': minified_items
    }

    return context
