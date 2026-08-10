from django.shortcuts import render, redirect# type: ignore
from .models import Category, Product, Customer, Order, Profile
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib import messages # type: ignore
from .forms import SignUpForm, UpdateUserForm, PasswordChangeForm, UserInfoFrom
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
import json
from Cart.cart import Cart
from payment.forms import ShippingAddressForm
from payment.models import ShippingAddress

# Create your views here.
def update_user(request):
    return render(request, 'update_user.html')

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories': categories})

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product' : product})

def category(request, foo):
    try:
        # 1. Fetch the category object
        category = Category.objects.get(name=foo)
        
        # 2. Filter using capital 'C' matching your models.py field definition
        products = Product.objects.filter(Category=category)
        
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        # 3. Pass `request` (HttpRequest) as the first argument to messages
        messages.error(request, 'That category does not exist.')
        return redirect('home')

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = Profile.objects.get(user__id=request.user.id)
            save_cart = current_user.old_cart
            if save_cart:
                converted = json.loads(save_cart)
                cart = Cart(request)
                for key, value in converted.items():
                    cart.db_add(product=key, quantity=value)    
            messages.success(request, 'You are successfully login')
            return redirect('home')
        else:
            messages.error(request, 'Authentication failed. Please try logging in.')
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

def registor_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  # use password1
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'continue fill info if you wnat to update your profile.')
                return redirect('update_profile')
            else:
                messages.error(request, 'Authentication failed. Please try logging in.')
                return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()

    return render(request, 'registor.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated:
        current_user = request.user  # or User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, 'Your account has been updated.')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.error(request, 'You must be logged in to update your account.')
        return redirect('login')
    


def update_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # keep user logged in
                messages.success(request, 'Your password has been updated.')
                return redirect('home')
            else:
                return render(request, 'password_update.html', {'form': form})
        else:
            form = PasswordChangeForm(user=request.user)
            return render(request, 'password_update.html', {'form': form})
    else:
        messages.error(request, 'You must be logged in to update your account.')
        return redirect('login')


def update_profile(request):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=request.user.id)
        shipping_user, created = ShippingAddress.objects.get_or_create(user=request.user)

        form = UserInfoFrom(request.POST or None, instance=current_user)
        shipping_form = ShippingAddressForm(request.POST or None, instance=shipping_user)

        if request.method == 'POST':
            if form.is_valid() and shipping_form.is_valid():
                form.save()
                shipping_form.save()
                messages.success(request, 'Your profile has been updated.')
                return redirect('home')
            else:
                messages.error(request, 'Please correct the errors below.')

        return render(request, 'update_profile.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.error(request, 'You must be logged in to update your account.')
        return redirect('login')
    
def search(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '')  # safe access
        if searched:  # only run query if not empty
            products = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
            if products.exists():
                return render(request, 'search.html', {'searched': searched, 'products': products})
            else:
                messages.error(request, 'No item found. Please try again.')
        else:
            messages.error(request, 'Please enter a search term.')
    return render(request, 'search.html')

