from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Sum
from django.db.models.functions import datetime
from django.forms import formset_factory
from django.http import JsonResponse

from .forms import PurchaseItemForm
from .models import Product, SaleInvoice, SoldItem, PurchasedItem, PurchaseInvoice
import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
import json


# Create your views here.

def home(request):
    return render(request, 'MainOrderApp/index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        pswconfirm = request.POST['pswconfirm']

        # Validations

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exists')
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, 'Email already registered')
            return redirect('signup')

        if len(username) > 10:
            messages.error(request, 'Username must be under 10 characters')
            return redirect('signup')

        if len(password) < 8:
            messages.error(request, 'Password must be longer than 8 characters')

            return redirect('signup')

        if password != pswconfirm:
            messages.error(request, 'Password confirmation does not match.')
            return redirect('signup')
        #
        # if not username.():
        #     messages.error(request, 'Username must be alphanumeric')
        #     return redirect('signup')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, 'Your account has been succesfuly created!')

        # # Welcome Email
        #
        # subject = 'Hello welcome to OderApp - SDA project'
        # message = 'Hello' + myuser.first_name + '!! \n' + 'Welcome to OrderAppInf\n' + 'Thank you for visiting out website.\n We have also sent you a confirmation Email. \n Please confirm your Email Adress'
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [myuser.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('signin')

    return render(request, 'MainOrderApp/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)  # Call login before redirecting
            fname = user.first_name
            messages.success(request, 'You have logged in successfully')
            return redirect('home')
        else:
            messages.error(request, 'Username or password do not match')
            return redirect('signin')

    return render(request, 'MainOrderApp/signin.html')


def signout(request):
    logout(request)
    messages.success(request, 'Logged out sucessfully')
    return redirect('home')


# views.py


def product_list(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            selected_products = data.get("selectedProducts", [])
            total_price = data.get("totalPrice", 0)  # Get total price from request data

            sale_invoice = SaleInvoice.objects.create(
                date=datetime.date.today(),
                time=datetime.datetime.now().time(),
                total_price=total_price,  # Use total price from request data
                user=request.user
            )

            for product_data in selected_products:
                product_id = product_data["productId"]
                quantity = product_data["quantity"]
                product = Product.objects.get(product_id=product_id)
                SoldItem.objects.create(
                    product=product,
                    quantity=quantity,
                    sale_invoice=sale_invoice
                )

            return JsonResponse({"message": "Checkout successful"}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    products = Product.objects.all()
    return render(request, 'MainOrderApp/product_list.html', {'products': products})


def inventory(request):
    # Query sold and purchased products
    sold_products = SoldItem.objects.all()
    purchased_products = PurchasedItem.objects.all()

    # Perform calculations and prepare inventory data
    inventory_data = {}
    for sold_product in sold_products:
        product_id = sold_product.product_id
        if product_id not in inventory_data:
            inventory_data[product_id] = {
                'product_id': product_id,
                'name': sold_product.product.name,
                'remaining_quantity': 0
            }
        inventory_data[product_id]['remaining_quantity'] -= sold_product.quantity

    for purchased_product in purchased_products:
        product_id = purchased_product.product_id
        if product_id not in inventory_data:
            inventory_data[product_id] = {
                'product_id': product_id,
                'name': purchased_product.product.name,
                'remaining_quantity': 0
            }
        inventory_data[product_id]['remaining_quantity'] += purchased_product.quantity

    sale_total_price = SaleInvoice.objects.aggregate(total=Sum('total_price'))['total']
    purchase_total_price = PurchaseInvoice.objects.aggregate(total=Sum('total_price'))['total']
    balance = sale_total_price - purchase_total_price

    # Render template with inventory data
    return render(request, 'MainOrderApp/inventory.html', {'inventory_data': inventory_data, 'balance': balance})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to keep the user logged in
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'MainOrderApp/change_password.html', {'form': form})


@transaction.atomic
def add_purchase_item(request):
    if request.method == 'POST':
        form = PurchaseItemForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            price = form.cleaned_data['price']
            total_price = int(quantity) * int(price)
            with transaction.atomic():
                # Create PurchaseInvoice instance
                purchase_invoice = PurchaseInvoice.objects.create(date=datetime.date.today(),
                                                                  time=datetime.datetime.now().time(),
                                                                  total_price=total_price,
                                                                  # Use total price from request data
                                                                  )
                # Create PurchasedItem instance
                purchased_item = PurchasedItem.objects.create(product=product, quantity=quantity, purchase_price=price,
                                                              purchase_invoice=purchase_invoice)
            return redirect('add_purchase_item')
    else:
        form = PurchaseItemForm()
    return render(request, 'MainOrderApp/add_purchase_item.html', {'form': form})
