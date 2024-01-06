from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.conf import settings
from django.http import HttpResponseRedirect,HttpResponse
# Create your views here.
from .models import Profile
from products.models import *
from accounts.models import *

import razorpay


def logout_page(request):
    logout(request)
    print("logging out")
    return redirect('/accounts/login')

def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if not user_obj.exists():
            messages.warning(request, 'Account not found.')
            return HttpResponseRedirect(request.path_info)


        if not user_obj[0].profile.is_email_verified:
            messages.warning(request, 'Your account is not verified.')
            return HttpResponseRedirect(request.path_info)

        user_obj = authenticate(username = email , password= password)
        print(user_obj)
        print("authenticated")
        if user_obj:
            login(request , user_obj)
            print("Logged in")
            print(user_obj.is_authenticated)

            return redirect('/')

        

        messages.warning(request, 'Invalid credentials')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/login.html')


def register_page(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = email)

        if user_obj.exists():
            messages.warning(request, 'Email is already taken.')
            return HttpResponseRedirect(request.path_info)

        print(email)

        user_obj = User.objects.create(first_name = first_name , last_name= last_name , email = email , username = email)
        user_obj.set_password(password)
        user_obj.save()

        messages.success(request, 'An email has been sent on your mail.')
        return HttpResponseRedirect(request.path_info)


    return render(request ,'accounts/register.html')




def activate_email(request, email_token):
    try:
        user = Profile.objects.get(email_token= email_token)
        user.is_email_verified = True
        user.save()
        return redirect('/accounts/login')
    except Exception as e:
        return HttpResponse('Invalid Email token')
    



def pop_price(price):
        try:
            return price.pop(0)
        except IndexError:
            return None

def cart(request):

    
    price=[]
    for a in CartItems.objects.all():
        price.append(a.get_product_price())
    prices_list=price
    
    context = {
        'cart_items_queryset': CartItems.objects.all(),
        'pop_price': pop_price,
        'prices_list': prices_list,
        'total':sum(price),
    }
    return render(request,'accounts/cart.html',context)


def remove_cart(request,uid):

    try:
        uid=uid[0:len(uid)-1]
        print(uid)
        cart_item=CartItems.objects.get(uid=uid)
        cart_item.delete()
        
    except Exception as e:
        print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def add_to_cart(request,uid):
    variant=request.GET.get('variant')
    product=Product.objects.get(uid=uid)
    user=request.user

    cart,_=Cart.objects.get_or_create(user=user,is_paid=False)

    cart_item=CartItems.objects.create(cart=cart,product=product)

    if variant:
        variant=request.GET.get('variant')
        size_variant=SizeVariant.objects.get(size_name=variant)
        cart_item.size_variant=size_variant
        cart_item.save()
        print("saved cart")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))