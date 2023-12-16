from django.http import HttpResponse
from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages #HIGLIGHT MESGGAES
from shop.form import CustomUserForm
from django.contrib.auth import authenticate,login,logout  #LOGIN CHECK





# Create your views here.
def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"shop/index.html",{"products":products})

def register(request):
    form=CustomUserForm()
    if request.method=="POST":
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Scucess")
            return redirect('/login')
    return render(request,"shop/register.html",{'form':form})


def loginpage(request):
    if request.user.is_authenticated:
        return redirect("/")
    else:
        if request.method=="POST":
            username = request.POST['username']
            password= request.POST['password']
            User=authenticate(request,username=username,password=password)
            if User is not None:
                login(request,User)
                messages.success(request,"Logged in Sucessfully")
                return redirect('/')
            else:
                messages.error(request,'Username or Password is incorrect')
        return render(request,"shop/login.html")

def logoutview(request):
    if request.user.is_authenticated:
        logout(request)  # Using the auth_logout function to log the user out
        messages.success(request, "Logged out Successfully")
    return redirect('/')

def collections(request):
    categories = Catagory.objects.filter(status=0) # Fetch all categories
    return render(request, "shop/collections.html", {'categories': categories})




def collectionsview(request, name):
    category = Catagory.objects.filter(name=name, status=0).first()

    if category:
        products = Product.objects.filter(catagory=category)
        return render(request, "shop/products/index.html", {'products': products, "C": name})
    else:
        messages.warning(request, "NO SUCH CATEGORY FOUND")
        return redirect('collections')



def productdetails(request,cname,pname):
    if(Catagory.objects.filter(name=cname,status=0)):
        if(Product.objects.filter(name=pname,status=0)).first():
            products=Product.objects.filter(name=pname,status=0).first()
            return render(request,"shop/products/productdetails.html",{"products":products})
        else:
             messages.warning(request, "NO SUCH Product FOUND")
             return redirect('collections')
    else:
         messages.warning(request, "NO SUCH CATEGORY FOUND")
         return redirect('collections')
          

    
