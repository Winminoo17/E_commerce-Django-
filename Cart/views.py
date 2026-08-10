from django.shortcuts import render,get_object_or_404
from .cart import Cart
from Eco_Website.models import Product
from django.http import JsonResponse 
from django.contrib import messages

# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.prods_cart()
    product_qty = cart.prods_qty()
    cart_total = cart.get_total_price()
    return render(request, 'cart_summary.html', {'cart_products': cart_products, 'product_qty' : product_qty, 'cart_total' : cart_total})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #look at in product DB
        product = get_object_or_404(Product, id = product_id)
        cart.add(product=product, quantity=product_qty)
        cart_qty = cart.__len__()
        response = JsonResponse({'qty':cart_qty})
        messages.success(request, 'Product added to cart.')
        return response
    
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        #lool at the database 
        cart.update_qty(product=product_id, qty=product_qty)
        response = JsonResponse({'qty':product_qty})
        messages.success(request, 'Product quantity updated.')
        return response
        
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.cart_delete(product=product_id)
        cart_qty = cart.__len__()
        response = JsonResponse({'qty':cart_qty})
        messages.success(request, 'Product removed from cart.')
        return response