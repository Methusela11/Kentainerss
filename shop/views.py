from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Product, ProductOption, CartItem, OrderItem, Order
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
    return render(request, "index.html", {"products": products})

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
    shipping_zone = request.POST.get("shipping_zone")  # ✅ ADD THIS

    product = get_object_or_404(Product, id=product_id)
    price = product.price
    option = None

    if option_id:
        option = get_object_or_404(ProductOption, id=option_id)
        price = option.price

    user = request.user if request.user.is_authenticated else None

    cart_item = CartItem.objects.filter(
        user=user,
        product=product,
        option=option,
        shipping_zone=shipping_zone   # ✅ INCLUDE THIS
    ).first()

    if cart_item:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        CartItem.objects.create(
            user=user,
            product=product,
            option=option,
            shipping_zone=shipping_zone,  # ✅ SAVE IT
            price=price,
            quantity=quantity
        )

    cart_items = CartItem.objects.filter(user=user)
    cart_subtotal = cart_items.aggregate(
        total=Sum(F("price") * F("quantity"))
    )["total"] or 0

    return render(
        request,
        "cart_sidebar.html",
        {
            "cart_items": cart_items,
            "cart_subtotal": cart_subtotal,
        },
    )


def remove_from_cart(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id)
        user = request.user if request.user.is_authenticated else None

        if cart_item.user == user:
            cart_item.delete()

        # Return updated cart HTML
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
    return JsonResponse({"error": "Invalid request"}, status=400)

def cart(request):
    user = request.user if request.user.is_authenticated else None

    cart_items = CartItem.objects.filter(user=user)

    cart_subtotal = 0
    cart_count = 0

    for item in cart_items:
        cart_subtotal += item.line_total
        cart_count += item.quantity

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'cart_count': cart_count,
            'cart_subtotal': cart_subtotal,
        }
    )


def cart_items_views(request):
    return render(request, "cart_items.html")

def checkout(request):
    user = request.user if request.user.is_authenticated else None
    cart_items = CartItem.objects.filter(user=user)

    if not cart_items.exists():
        return redirect("cart")

    total = Decimal("0.00")

    for item in cart_items:
        total += item.price * item.quantity

    if request.method == "POST":

        # ✅ Create Order from billing form
        order = Order.objects.create(
            user=user,

            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            company=request.POST.get("company"),

            street=request.POST.get("street"),
            city=request.POST.get("city"),
            county=request.POST.get("county"),
            postcode=request.POST.get("postcode"),

            phone=request.POST.get("phone"),
            email=request.POST.get("email"),

            total_amount=total
        )

        # ✅ Save order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                option=item.option,
                product_name=item.product.name,
                option_name=item.option.name if item.option else "",
                price=item.price,
                quantity=item.quantity
            )

        # # OPTIONAL: Clear cart
        # cart_items.delete()

        # ✅ Redirect to payment page
        return redirect("payment_page", order_id=order.id)

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": total
    })

@require_POST
def update_cart_quantity(request, item_id):
    action = request.POST.get("action")
    cart_item = get_object_or_404(CartItem, id=item_id)

    user = request.user if request.user.is_authenticated else None

    if cart_item.user != user:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease" and cart_item.quantity > 1:
        cart_item.quantity -= 1

    cart_item.save()

    return JsonResponse({
        "success": True,
        "quantity": cart_item.quantity,
    })

def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, "payment.html", {
        "order": order
    })

def choose_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, "choosepayment.html", {
        "order": order
    })

@csrf_exempt
def update_basket(request):
    if request.method == "POST":
        data = json.loads(request.body)
        updates = data.get("updates", [])
        user = request.user if request.user.is_authenticated else None

        subtotal = 0

        for item in updates:
            cart_item = CartItem.objects.filter(id=item["id"], user=user).first()
            if cart_item:
                cart_item.quantity = int(item["quantity"])
                cart_item.save()
                subtotal += cart_item.line_total

        subtotal_display = f"{intcomma(int(subtotal))} KES"

        return JsonResponse({"success": True, "cart_subtotal": subtotal_display})

    return JsonResponse({"success": False}, status=400)

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