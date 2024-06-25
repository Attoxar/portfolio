from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Order, Product, OrderItem
from .forms import ContactForm, TargetForm
from .utils import (
    port_scanning,
    website_vulnerabilities,
    looking_up_dns,
    traceroute_view,
    os_detection,
)

# Constants for payloads and sensitive files
SQL_INJECTION_PAYLOADS = ("'", "' OR 1=1 --", '" OR 1=1 --', "' OR 'a'='a'")
CROSS_SITE_SCRIPT = ("<script>alert(1)</script>", "<img src=x onerror=alert(1)>")
LOCAL_FILE_INJECTION = ("../../../../etc/passwd", "../../../../windows/win.ini")
SENSITIVE_FILES = (".git", ".env", "config.php", "backup.zip", "backup.sql")


def home(request):
    return render(request, "home.html")


def portfolio(request):
    return render(request, "portfolio.html")


def shop(request):
    products = Product.objects.all()
    return render(request, "shop.html", {"products": products})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error_message = "Invalid credentials"
            return render(request, "login.html", {"error_message": error_message})
    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def cart(request):
    order_items = OrderItem.objects.filter(user=request.user, ordered=False)
    total_price = sum(item.get_total_item_price() for item in order_items)
    return render(
        request, "cart.html", {"order_items": order_items, "total_price": total_price}
    )


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, ordered=False)
    order_item, item_created = OrderItem.objects.get_or_create(
        order=order, product=product, ordered=False
    )
    if not item_created:
        order_item.quantity += 1
        order_item.save()
    return redirect("cart")


@login_required
def checkout(request):
    order_items = OrderItem.objects.filter(order__user=request.user, ordered=False)
    total_price = sum(item.get_total_item_price() for item in order_items)

    context = {
        'order_items': order_items,
        'total_price': total_price,
    }
    return render(request, 'checkout.html', context)


@login_required
def remove_from_cart(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id)
    order_item.delete()
    return redirect("cart")


@login_required
def cart(request):
    order = Order.objects.get(user=request.user, ordered=False)
    order_items = OrderItem.objects.filter(order=order)

    context = {
        "order": order,
        "order_items": order_items,
    }

    return render(request, "cart.html", context)


def product_list(request):
    products = Product.objects.all()
    return render(request, "shop/product_list.html", {"products": products})


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["username"]
            message = form.cleaned_data["message"]
            from_email = form.cleaned_data["email"]
            recipient_list = ["andreas.blanck@ymail.com"]
            send_mail(subject, message, from_email, recipient_list)
            return redirect("contact_success")
    else:
        form = ContactForm()
    return render(request, "contact.html", {"form": form})


def contact_success(request):
    return render(request, "contact_success.html")


@login_required
def intelligence_gathering(request):
    result = None
    if request.method == "POST":
        form = TargetForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data["target"]
            option = form.cleaned_data["intelligence_option"]

            if option == "port_scan":
                result = port_scanning(target)
            elif option == "web_scan":
                result = website_vulnerabilities(target)
            elif option == "dns_lookup":
                result = looking_up_dns(target)
            elif option == "traceroute":
                result = traceroute_view(target)
            elif option == "os_detection":
                result = os_detection(target)
    else:
        form = TargetForm()

    return render(
        request, "intelligence_gathering.html", {"form": form, "result": result}
    )


@login_required
def port_scan(request):
    result = None
    if request.method == "POST":
        form = TargetForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data["target"]
            result = port_scanning(target)
    else:
        form = TargetForm()
    return render(request, "port_scan.html", {"form": form, "result": result})


@login_required
def web_scan(request):
    result = None
    if request.method == "POST":
        form = TargetForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data["target"]
            result = website_vulnerabilities(target)
    else:
        form = TargetForm()
    return render(request, "web_scan.html", {"form": form, "result": result})


@login_required
def dns_lookup(request):
    result = None
    if request.method == "POST":
        form = TargetForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data["target"]
            result = looking_up_dns(target)
    else:
        form = TargetForm()
    return render(request, "dns_lookup.html", {"form": form, "result": result})


@login_required
def traceroute(request):
    result = None
    if request.method == "POST":
        form = TargetForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data["target"]
            result = traceroute_view(target)
    else:
        form = TargetForm()
    return render(request, "traceroute.html", {"form": form, "result": result})


@login_required
def detect_os(request):
    result = None
    if request.method == "POST":
        form = TargetForm(request.POST)
        if form.is_valid():
            target = form.cleaned_data["target"]
            result = os_detection(target)
    else:
        form = TargetForm()
    return render(request, "detect_os.html", {"form": form, "result": result})


def about_me(request):
    return render(request, 'about_me.html')


def multimedia(request):
    context = {
        # maybe puting in some kind of discription comments etc
    }
    return render(request, 'multimedia.html', context)
