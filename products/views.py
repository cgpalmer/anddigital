from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from .models import Product
from .forms import ProductForm
import qrcode  #https://betterprogramming.pub/how-to-generate-and-decode-qr-codes-in-python-a933bce56fd0
from PIL import Image

# Create your views here.
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
            qr.add_data('https://cpalmer-andi-golden-shoe.herokuapp.com/')
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