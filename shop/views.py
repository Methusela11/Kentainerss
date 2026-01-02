from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductOption, CartItem
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import F, Sum

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

    has_options = product.options.exists()

    # Product classification
    is_viable = product.type == "viable" and has_options
    is_simple = product.type == "simple" and not has_options

    # Related products (same category, exclude current)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)

    context = {
        "product": product,
        "options": product.options.all() if has_options else None,
        "is_viable": is_viable,
        "is_simple": is_simple,
        "related_products": related_products,
    }

    return render(request, "product.html", context)


def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("shop")

    option_id = request.POST.get("option_id")
    quantity = int(request.POST.get("quantity", 1))

    product = get_object_or_404(Product, id=product_id)
    price = product.price
    option = None

    if option_id:
        option = get_object_or_404(ProductOption, id=option_id)
        price = option.price

    user = request.user if request.user.is_authenticated else None

    # Try to get existing cart item
    cart_item = CartItem.objects.filter(
        user=user,
        product=product,
        option=option
    ).first()

    if cart_item:
        cart_item.quantity += quantity
        cart_item.price = price
        cart_item.save()
    else:
        CartItem.objects.create(
            user=user,
            product=product,
            option=option,
            price=price,
            quantity=quantity
        )

    cart_items = CartItem.objects.filter(user=user)
    cart_subtotal = cart_items.aggregate(total=Sum(F("price") * F("quantity")))["total"] or 0

    return render(
        request,
        "cart_sidebar.html",
        {
            "cart_items": cart_items,
            "cart_subtotal": cart_subtotal,
        },
    )

def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_count = sum(item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_count': cart_count})

def cart_items_views(request):
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