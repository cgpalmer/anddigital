from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product

from django.contrib import messages


# Returning the user's basket
def view_basket(request):
    return render(request, 'basket/basket.html')


''' This add_to_basket function will add a product to the basket. It receive the information from a form,
    store the information in a json and then save the basket.
    It has several feature checks along the way: type of delivery, any linked products?,
    checking for duplicated linked products. Linked products are photographs that can
    be added to a container purchase.'''


def add_to_basket(request, item_id):
    if request.method == 'POST':
        # Requesting basket information
        basket = request.session.get('basket', {})
        basket_item_id = request.session.get('basket_item_id')

        # Retrieving form data
        quantity = int(request.POST.get('quantity'))
        product = get_object_or_404(Product, pk=item_id)
        size = int(request.POST.get('size'))

        if basket != {}:
            current_basket_total = 0
            for item in basket['items']:
                current_basket_total = current_basket_total + 1

            basket_item_id = current_basket_total + 1            
            basket['items'].append({
                'basket_item_id': basket_item_id,
                'item_id': item_id,    
                'quantity': quantity,
                'size': size,
                })
        else:
            basket['items'] = []
            request.session['basket_item_id'] = 1
            basket['items'].append({
                'basket_item_id': 1,
                'item_id': item_id,
                'quantity': quantity,
                'size': size,
            })

        redirect_url = request.POST.get('redirect_url')
        request.session['basket'] = basket
        messages.success(request, f"Successfully added '{product.friendly_name}' to your basket.")
    else:
        redirect_url = 'home/index.html'
    return redirect(redirect_url)


def edit_basket(request):
    basket = request.session.get('basket', {})
    updated_quantity = request.POST.get('basket_quantity')
    updated_delivery = request.POST.get('basket_digital_download')
    basket_item_id = request.POST.get('basket_item_id')

    # Getting variables to set up editing the linked photos
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, pk=product_id)
    item_number = -1
    for item in basket['items']:
        item_number = item_number + 1
        if int(basket_item_id) == item['basket_item_id']:
            # Updating the quantity
            if int(updated_quantity) == 0:
                del basket['items'][item_number]
            else:
                item['quantity'] = int(updated_quantity)

            # Updating the digital download if necessary
            if product.digital_download is True:
                if updated_delivery == "True":
                    item['digital_download'] = 'on'
                    item['quantity'] = 1
                    messages.warning(request, "Digital purchases are restricted to a quantity of 1.")
                else:
                    item['digital_download'] = None

            # Checking if editing the basket had changed the linked products
            updated_linked_product_images_list = []
            updated_linked_products = []
            if product.number_of_pictures > 0:
                for i in range(product.number_of_pictures):
                    linked_product_details = request.POST.get('edit-linked-product' + str(i))
                    split_linked_product_details = linked_product_details.split("|")
                    linked_product_id = split_linked_product_details[1]
                    linked_product_image = split_linked_product_details[0]
                    linked_product_type = split_linked_product_details[2]

                    # Changing media paths depending if the user is using their own photo.
                    if linked_product_type == "upload":
                        linked_product_image = "/media/" + linked_product_image
                        updated_linked_product_images_list.append(linked_product_image)
                    else:
                        updated_linked_product_images_list.append(linked_product_image)

                    if linked_product_id == "No id":
                        linked_product = 'Not linked'
                    elif linked_product_type == 'upload':
                        linked_product_object = get_object_or_404(Image_upload, pk=linked_product_id)
                        linked_product = linked_product_object.sku
                    else:
                        linked_product_object = get_object_or_404(Product, pk=linked_product_id)
                        linked_product = linked_product_object.sku

                    if updated_linked_products != []:
                        updated_linked_products.append(linked_product)
                    else:
                        updated_linked_products.insert(0, linked_product)
            else:
                updated_linked_products = ['Not available']
                updated_linked_product_images_list = ['Not available']
            item['linked_products'] = updated_linked_products
            item['linked_product_images_list'] = updated_linked_product_images_list

    request.session['basket'] = basket
    return redirect('view_basket')


def delete_basket_item(request, basket_item_id):
    basket = request.session.get('basket', {})
    basket_item_id = int(basket_item_id)
    item_number = -1
    for item in basket['items']:
        item_number = item_number + 1
        if item['basket_item_id'] == basket_item_id:
            del basket['items'][item_number]
            request.session['basket'] = basket
    return redirect('view_basket')


def empty_basket(request):
    emptyingBasket(request)
    return redirect('view_basket')


def emptyingBasket(request):
    basket = request.session.get('basket', {})
    if basket != {}:
        del basket['items']
        request.session['basket'] = basket
    return basket
