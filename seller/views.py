from django.shortcuts import render,redirect
from django.conf import settings
from django.core.mail import send_mail
from random import randint
from .models import *
from django.core.files.uploadedfile import InMemoryUploadedFile
import os


# Get Active User.....

def seller_active(request):
      global seller_details
      seller_details = Seller.objects.get(email= request.session['seller_email'] )

def send_otp(request):
    global c_otp
    c_otp = randint(100000,999999)
    sub = f"Seller Email Verification Code : {c_otp}"
    message = f"Use This Code to finish setting up ypur account:\n{c_otp}\n\n This code will expire in 10 mins"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [seller_data['email']]
    send_mail(sub,message,from_email,recipient_list)

#................................HOME Page...........................


def seller_index(request):
    try:
        seller_active(request)
        products = Product.objects.filter(seller = seller_details)
        return render(request ,'seller_index.html',{'seller_details':seller_details,'products':len(products)})
    except:
        return render(request,'seller_register.html')


# ................................Authentication...........................

def seller_login(request):
    if request.method == 'GET':
        try:
            seller_active(request)
            return redirect('seller_index')
        except:
            return render(request,'seller_login.html')
    else:
        try:
            seller_data = Seller.objects.get(email = request.POST['email'])
            if seller_data.password == request.POST['password']:
                request.session['seller_email'] = request.POST['email']
                return redirect('seller_index')
            else:
                return render(request , 'seller_login.html',{'msg':"Password Invlid"})
        except:
            return render(request , 'seller_login.html',{'msg':"Seller Does Not Exsist"})

def seller_register(request):
    if request.method == 'GET':
        return render(request,'seller_register.html')
    else:
        try:
            Seller.objects.get(email = request.POST['email'])
            return render(request,'seller_register.html',{'msg':'User Exsist'})
        except:
            if request.POST['password'] == request.POST['cpassword']:
                global seller_data
                seller_data = {
                    'shop_name' : request.POST['shop_name'] ,
                    'name' : request.POST['name'],
                    'email' : request.POST['email'],
                    'password' : request.POST['password'],
                    'gst_no' : request.POST['gst_no']
                 }
                send_otp(request)
                return render(request,'seller_verification.html',{'msg' : "Enter Code Sent to Your Email."} )
            else:
                return render(request,'seller_register.html',{'msg':'Both Passwords do not match'})

def resend_otp(request):
    send_otp(request)
    return render(request,'seller_verification.html',{'msg' : "Enter Code Sent to Your Email."} )

def seller_verification(request):
    if request.POST['u_otp'] == str(c_otp):
        Seller.objects.create(
            shop_name =seller_data['shop_name'],    
            name =seller_data['name'],
            email = seller_data['email'],
            password = seller_data['password'],
            gst_no = seller_data['gst_no']
        )
        return render(request, 'seller_login.html',{'msg':'Account Created'})
    else:
        return render(request,'seller_verification.html',{'msg':'Invalid OTP'})

def seller_logout(request):
    del request.session['seller_email']
    return redirect('seller_login')

def profile(request):
    try:
        seller_active(request)
        return render(request ,'seller_profile.html',{'seller_details':seller_details,'disabled':'disabled','method':'get'})
    except:
        return render(request,'seller_profile.html')

def edit_details(request):
    seller_active(request)
    if request.method == "GET":
        return render(request,'seller_profile.html',{'seller_details':seller_details,'disabled':'','method':'post'})
    else:
        seller_details.shop_name = request.POST['shop_name']
        seller_details.name = request.POST['name']
        seller_details.gst_no = request.POST['gst_no']
        if request.FILES:
            seller_details.profile_pic = request.FILES['profile_pic']
        seller_details.save()
        return render(request ,'seller_profile.html',{'seller_details':seller_details,'disabled':'disabled','method':'get'})


#................................Product CRUD...........................

def add_product(request):
    if request.method == "GET":
        try:
            seller_active(request)
            return render(request, 'add_product.html',{'seller_details':seller_details,'task':'Add'})
        except:
            return render(request, 'seller_login.html')
    else:
        try:
            seller_active(request)
            seller_obj = Seller.objects.get(email = request.session['seller_email'])
            Product.objects.create(
                product_name = request.POST['product_name'],
                desc = request.POST['desc'],
                price = request.POST['price'],
                product_stock = request.POST['product_stock'],
                product_pic = request.FILES['product_pic'],
                seller = seller_obj
            )
            return render(request, 'add_product.html',{'msg':'Product Added','task':'Add'})
        except:
            return render(request, 'add_product.html',{'task':'Add'})

def products(request):
    try:
        seller_active(request)
        productlist = Product.objects.filter(seller = seller_details)
        return render(request, 'seller_product.html',{'seller_details':seller_details,'productlist':productlist})
    except:
        return render(request, 'seller_product.html')

def edit_product(request,pk):
    product = Product.objects.get(id = pk)
    if request.method == 'GET':
        seller_active(request)
        return render(request, 'add_product.html', {'seller_details':seller_details,'task':'EDIT','product':product})
    else:
        product.product_name = request.POST['product_name']
        product.desc = request.POST['desc']
        product.price = request.POST['price']
        product.product_stock = request.POST['product_stock']
        if request.FILES:
            product.product_pic = request.FILES['product_pic']
        product.save()
        return redirect('products')

def delete_product(request,pk):
    product = Product.objects.get(id = pk)
    product.delete()
    return redirect('products')

#.........................................Order Manage................................
def recent_order(request):
    seller_active(request)
    orderlist = MyOrder.objects.filter(product__seller = seller_details,status = "P") 
    return render(request, 'recent_order.html',{'seller_details':seller_details,'orderlist':orderlist})

def completed_order(request):
    seller_active(request)
    orderlist = MyOrder.objects.filter(product__seller = seller_details,status = "D") 
    return render(request, 'completed_order.html',{'seller_details':seller_details,'orderlist':orderlist})

def dispatch(request,pk):
    order = MyOrder.objects.get(id = pk)
    order.status = "D"
    order.save()
    return redirect('order_history')


# ...................................Charts,Maps.......................................

def charts(request):
    return render(request,'charts.html')

def map(request):
    return render(request,'maps.html')


# def del_seller(request):
#       seller_obj = Seller.objects.get(email='')
#       seller_obj.delete()
#       return HttpResponse("seller Deleted")

