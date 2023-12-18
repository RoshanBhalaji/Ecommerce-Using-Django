import json
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages  # Highlight messages
from shop.form import *
from django.contrib.auth import authenticate, login, logout  # Login check

from django.db import transaction


def home(request):
    products = Product.objects.filter(trending=1)
    return render(request, "shop/index.html", {"products": products})


def register(request):
    form = CustomUserForm()
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Success")
            return redirect('/login')
    return render(request, "shop/register.html", {'form': form})


def loginpage(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            User = authenticate(request, username=username, password=password)
            if User is not None:
                login(request, User)
                messages.success(request, "Logged in Successfully")
                return redirect('/')
            else:
                messages.error(request, 'Username or Password is incorrect')
        return render(request, "shop/login.html")


def logoutview(request):
    if request.user.is_authenticated:
        logout(request)  # Using the auth_logout function to log the user out
        messages.success(request, "Logged out Successfully")
    return redirect('/')


def Feedback(request):
     # Initialize success_message as None

    if request.method == 'POST':
        feedbackform = Feedbackform(request.POST)
        if feedbackform.is_valid():
            feedbackform.save()
            messages.success(request, "Feedback submitted successfully")

    else:
        feedbackform = Feedbackform()

    return render(request, 'shop/feedback.html', {'feedbackform': Feedback})


def collections(request):
    categories = Catagory.objects.filter(status=0)  # Fetch all categories
    return render(request, "shop/collections.html", {'categories': categories})


def collectionsview(request, name):
    category = Catagory.objects.filter(name=name, status=0).first()

    if category:
        products = Product.objects.filter(catagory=category)
        return render(request, "shop/products/index.html", {'products': products, "C": name})
    else:
        messages.warning(request, "NO SUCH CATEGORY FOUND")
        return redirect('collections')


def productdetails(request, cname, pname):
    if Catagory.objects.filter(name=cname, status=0):
        if Product.objects.filter(name=pname, status=0).first():
            products = Product.objects.filter(name=pname, status=0).first()
            return render(request, "shop/products/productdetails.html", {"products": products})
        else:
            messages.warning(request, "NO SUCH Product FOUND")
            return redirect('collections')
    else:
        messages.warning(request, "NO SUCH CATEGORY FOUND")
        return redirect('collections')
    
def cart_page(request):
   if request.user.is_authenticated:
      Cart1=Cart.objects.filter(user=request.user)
      return render(request, "shop/cart.html", {'cart':Cart1})
   else:
      return redirect('/')

@transaction.atomic # handle Db lock
def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      product_status=Product.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)


def remove_cart(request, id):
    cart_item = Cart.objects.filter(id=id)
    cart_item.delete()
    return redirect("/cart")

