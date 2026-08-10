from django.shortcuts import render, redirect
from Cart.cart import Cart
from payment.forms import ShippingAddressForm, PaymentForm
from payment.models import ShippingAddress, OrderModel, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from Eco_Website.models import Product, Profile
import datetime

# Create your views here.
def payment_success(request):
    return render(request, 'payment/payment_success.html')

def checkout(request):
    cart = Cart(request)
    cart_products = cart.prods_cart()
    cart_qty = cart.prods_qty()
    cart_total = cart.get_total_price()
    print(request.user.id)
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        form = ShippingAddressForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'cart_qty' : cart_qty, 'cart_total' : cart_total, 'form': form})
    else:
        form = ShippingAddressForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products': cart_products, 'cart_qty' : cart_qty, 'cart_total' : cart_total, 'form': form})
    
def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.prods_cart()
        cart_qty = cart.prods_qty()
        cart_total = cart.get_total_price()
        
        my_shipping = request.POST
        request.session['shipping'] = my_shipping
        
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products': cart_products, 'cart_qty' : cart_qty, 'cart_total' : cart_total, 'shipping_form': request.POST, 'billing_form': billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {'cart_products': cart_products, 'cart_qty' : cart_qty, 'cart_total' : cart_total, 'shipping_form': request.POST, 'billing_form': billing_form})
        shipping_form = request.POST
        return render(request, 'payment/billing_info.html', {'cart_products': cart_products, 'cart_qty' : cart_qty, 'cart_total' : cart_total, 'shipping_form': shipping_form})
    else:
        messages.error(request, 'Please enter shipping information.')
        return render(request, 'payment/billing_info.html')
    
def process_order(request):
    if request.method != 'POST':
        messages.error(request, 'Please enter billing information.')
        return redirect('home')

    payment_form = PaymentForm(request.POST)
    my_shipping = request.session.get('shipping', {})
    cart = Cart(request)
    cart_products = cart.prods_cart()
    cart_qty = cart.prods_qty()          # {'3': 2, '5': 1, ...}
    cart_total = cart.get_total_price()

    full_name = my_shipping.get('shipping_full_name')
    email = my_shipping.get('shipping_email')
    address = my_shipping.get('shipping_address')
    amount_paid = cart_total

    user = request.user if request.user.is_authenticated else None

    create_order = OrderModel(
        user=user,
        full_name=full_name,
        email=email,
        shipping_address=address,
        amount_paid=amount_paid,
    )
    create_order.save()

    for product in cart_products:
        qty = cart_qty.get(str(product.id))
        if not qty:
            continue
        price = product.sale_price if product.is_sale else product.price
        OrderItem.objects.create(
            order=create_order,
            product=product,
            user=user,
            quantity=qty,
            price=price,
        )

    # ...after the OrderItem loop...

    cart.clear()
    if 'shipping' in request.session:
        del request.session['shipping']
        
    current_user = Profile.objects.filter(user__id=request.user.id)
    current_user.update(old_cart=None)

    messages.success(request, 'Your order has been processed.')
    return redirect('payment_success')


def not_shipped_dash(request):
    
    if request.user.is_authenticated:
        orders = OrderModel.objects.filter(shipped=False)
        if request.method == 'POST':
            status = request.POST['status']
            order_id = request.POST['order_id']
            if status == 'true':
                order = OrderModel.objects.filter(id=order_id)
                now = datetime.datetime.now()
                order.update(shipped=True, date_ship=now)
                messages.success(request, 'Order Status Updated as shipped')
        return render(request, 'payment/not_shipped_dash.html', {'orders':orders})
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')
    

def shipped_dash(request):
    if request.user.is_authenticated:
        orders = OrderModel.objects.filter(shipped=True)
        if request.method == 'POST':
            status = request.POST['status']
            order_id = request.POST['order_id']
            if status == 'false':
                order = OrderModel.objects.filter(id=order_id)
                order.update(shipped=False)
                messages.success(request, 'Order Status Updated as Un shipped')
        return render(request, 'payment/shipped_dash.html', {"orders":orders})
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')
    
def order(request, pk):
    if request.user.is_authenticated:
        order = OrderModel.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        if request.method == 'POST':
            status = request.POST['status']
            if status == 'true':
                order = OrderModel.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=True, date_ship=now)
            else:
                order = OrderModel.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request, 'Order Status Updated')
            return redirect('not_shipped_dash')
            
        return render(request, 'payment/order.html', {'order':order, 'items':items})
    else:
        messages.success(request, 'Access Denied')
        return redirect('home')