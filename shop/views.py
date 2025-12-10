from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductOption, CartItem
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Signup
def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created! Please log in.")
            return redirect('login')
    return render(request, 'signup.html')

# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # change to your main page
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    products = Product.objects.order_by('-id')[:10]  # fetch latest 10
    return render(request, "home.html", {"products": products})

def shop(request):
    products = Product.objects.all()
    return render(request, "shop.html", {"products": products})



def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    # Options for "viable" product types
    sizes = product.options.all().order_by("price") if product.type == "viable" else None

    return render(request, "product.html", {
        "product": product,
        "sizes": sizes,     # <-- FIXED HERE!
    })



@login_required
def add_to_cart(request, product_id):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        option_id = request.POST.get("option_id")
        quantity = int(request.POST.get("quantity"))

        product = Product.objects.get(id=product_id)

        if product.type == "variable":
            option = ProductOption.objects.get(id=option_id)
            price = option.price
            label = option.name
        else:
            price = product.price
            label = None

        CartItem.objects.create(
            user=request.user,  # Assign logged-in user
            product=product,
            option_label=label,
            price=price,
            quantity=quantity
        )
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return render(request, "cart_items.html", {"cart": cart})

        return redirect("cart_page")

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_count = sum(item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_count': cart_count})

def cart_items(request):
    return render(request, "cart_items.html")

def water_tank_storage(request):
    # Filter products by category
    products = Product.objects.filter(category="water_tanks")
    context = {
        'products': products
    }
    return render(request, 'watertankstorage.html', context)

def sanitation_storage(request):
    products = Product.objects.filter(category="sanitation_storage")
    context = {
        'products': products
    }
    return render(request, 'sanitation.html', context)

def agriculture(request):
    products = Product.objects.filter(category="agriculture")
    context = {
        'products': products
    }
    return render(request, 'agriculture.html', context)

def material_handling(request):
    products = Product.objects.filter(category="material_handling")
    context = {
        'products': products
    }
    return render(request, 'materialhandling.html', context)

def water_supply_and_accessories(request):
    products = Product.objects.filter(category="water_supply_and_accessories")
    context = {
        'products': products
    }
    return render(request, 'watersupplyandaccessories.html', context)

def special_products_and_others(request):
    products = Product.objects.filter(category="special_products")
    context = {
        'products': products
    }
    return render(request, 'specialproducts.html', context)