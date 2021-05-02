from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from .models import Product, Product_stock
from customer_service.models import Store
from .forms import ProductForm, Product_stockForm
import qrcode  #https://betterprogramming.pub/how-to-generate-and-decode-qr-codes-in-python-a933bce56fd0
from PIL import Image

# Create your views here.
def all_products(request):
    # Returning the products page
    products = Product.objects.all()
    query = None
    categories = None
    special_offer = None
    sort = None
    direction = None

    # Getting search queries from the URL
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))

            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

    if request.GET:
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)
    if request.GET:
        if 'special_offer' in request.GET:
            special_offer = request.GET['special_offer'].split(',')
            if special_offer == ['no_offer']:
                products = products.exclude(special_offer__name__in=special_offer)
            else:
                products = products.filter(special_offer__name__in=special_offer)
            special_offer = Special.objects.filter(name__in=special_offer)

    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria.")
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query) | Q(
                friendly_name__icontains=query) | Q(sku__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
        'special_offer': special_offer
    }
    return render(request, 'products/products.html', context)










def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            retrieval = form.cleaned_data.get("qr_retrieval_key")
            form.save()
            product = get_object_or_404(Product, qr_retrieval_key=retrieval)
            print(product.name)
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(f'https://cpalmer-andi-golden-shoe.herokuapp.com/products/{product.id}')
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            qr_path = f"static/qr/{product.id}{product.name}.png"
            img.save(qr_path)
            product.qr_code = f"/static/qr/{product.id}{product.name}.png"


            product.save()
            # insert new qr code here

            return redirect(reverse('home'))
        else:
            messages.error(
                request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


def product_detail(request, product_id):
    # Returning the details of a specific product.
    product = get_object_or_404(Product, pk=product_id)
    sizes = Product_stock.objects.filter(product=product).order_by("size")
    store_search = get_object_or_404(Store, store_name="Online")
    available_sizes = Product_stock.objects.filter(store=store_search).distinct("size")
    stores = Product_stock.objects.filter(product=product).distinct("store")
    print(sizes)
    print(product.images[0])
    display_image = (product.images[0])
    context = {
        'product': product,
        'sizes': sizes,
        'available_sizes': available_sizes,
        'stores': stores,
        'display_image': display_image
    }
    return render(request, 'products/product_detail.html', context)



def add_product_stock(request):
    
    if request.method == 'POST':
        form = Product_stockForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form_product = form.cleaned_data.get("product")
            form_stock_levels = form.cleaned_data.get("stock_levels")
            location = form.cleaned_data.get("store")
            print(location)
            print(type(location))
            print(location.store_name)
            print(type(location.store_name))
            product = get_object_or_404(Product, pk=form_product.id)
            if location.store_name == "Online":
                product.online_stock_count = product.online_stock_count + form_stock_levels
            else:
                product.store_stock_count = product.store_stock_count + form_stock_levels
            product.save()
            return redirect(reverse('home'))
        else:
            messages.error(
                request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = Product_stockForm()
    template = 'products/add_product_stock.html'
    context = {
        'form': form,
    }
    return render(request, template, context)
        

