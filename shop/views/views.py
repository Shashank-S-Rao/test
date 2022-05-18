from django.shortcuts import redirect,render
from django.contrib.auth import login,logout,authenticate
from shop.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from shop.models.models import *
import os
# Create your views here.

fileDir = os.path.dirname(os.path.realpath(__file__))
# fileDir = os.path.dirname(fileDir)
split = fileDir.split('/')
media_dir = os.path.join(fileDir, 'images')

def home(request):
    print(request.user.id)
    products = Product.objects.all()
    context = {
        'products':products,
        'request':request
    }
    print(request)
    return render(request,'home.html',context)

def placeOrder(request,i):
    customer= Customer.objects.get(id=i)
    form=createorderform(instance=customer)
    if(request.method=='POST'):
        form=createorderform(request.POST,instance=customer)
        if(form.is_valid()):
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'placeOrder.html',context)


def addProduct(request):
    form=createproductform()
    if(request.method=='POST'):
        form=createproductform(request.POST,request.FILES)
        if(form.is_valid()):
            form.save()
            return HttpResponseRedirect('shop/home')
    context={'form':form}
    return render(request,'addProduct.html',context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form=createuserform()
        customerform=createcustomerform()
        if request.method=='POST':
            form=createuserform(request.POST)
            customerform=createcustomerform(request.POST)
            if form.is_valid() and customerform.is_valid():
                user=form.save()
                customer=customerform.save(commit=False)
                customer.user=user
                customer.save()
                return redirect('login')
        context={
            'form':form,
            'customerform':customerform,
        }
        return render(request,'register.html',context)

def loginPage(request):
    print('login')
    if request.user.is_authenticated:
        return HttpResponseRedirect('/shop/home')
    else:
       if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect('/shop/home')
       context={}
       return render(request,'login.html',context)

def logoutPage(request):
    logout(request)
    return HttpResponseRedirect('/shop/login')

def download_media(request, filename):
    if request.method == 'GET':
        print('dir_name',media_dir)
        file_name_to_download = os.path.join(media_dir,filename)
        print(file_name_to_download)
        if os.path.exists(file_name_to_download):
            with open(file_name_to_download, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="image/jpg")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_name_to_download)
                return response
        else:
            # log_obj.debug('download_media:file does not exists')
            return HttpResponse("File does not exists", status=404)

def addToCart(request,pid,cid):
    print(Customer.objects.all().values())
    print(cid)
    product = Product.objects.get(id=pid)
    user = User.objects.get(id=cid)
    form = quantityForm(request.POST)
    if request.method=="POST":
        if form.is_valid():
            data=form.cleaned_data
            quantity = data['quantity']
            try:
                print("create")
                customer = Customer.objects.get(user=user)
                Cart.objects.create(product=product, customer=customer, quantity=quantity)
                return HttpResponse("Success")
            except Costumer.DoesNotExist:
                print("update")
                customer = Customer.objects.create(name=user.username, user=user)
                Cart.objects.create(product=product,customer=customer,quantity=quantity)
                return HttpResponse("Success")
        else:
            print(form.errors)
            return HttpResponse("failure")
    else:
        print("GET!!")
        return HttpResponse("Failure")


def getCartItem(request,cid):
    print(cid)
    user = User.objects.get(id=cid)
    costumer_id = Customer.objects.get(user=user)
    cart_item = Cart.objects.filter(customer=costumer_id.id)
    p_id=cart_item.values_list('product_id')
    product=Product.objects.filter(id__in=p_id).values()
    print(product)
    return render(request,'Cart.html',{'cart_items':cart_item})

def checkout(request,cid):
    user = User.objects.get(id=cid)
    costumer_id = Customer.objects.get(user=user)
    cart_item = Cart.objects.filter(customer=costumer_id.id)
    print(cart_item)
    ids=[]
    for i in cart_item:
        checkout = Checkout.objects.create(cart_item=i)
        ids.append(checkout.id)
    print(ids)
    checkout = Checkout.objects.filter(id__in=ids)
    return render(request,'checkout.html',{'checkout_items':checkout})


