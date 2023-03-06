from django.shortcuts import render, redirect
from .models import *
from seller.models import *
from random import randint
from django.core.mail import send_mail
from django.conf import settings
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest,JsonResponse
# from django.http import HttpResponse


# .............................Active User............................
def active(request):
    global active_user
    active_user = Buyer.objects.get(email=request.session['email'])


def index(request):
    products = Product.objects.all()
    try:
        active(request)
        return render(request, 'index.html', {'active_user': active_user, 'products': products})
    except:
        return render(request, 'index.html', {'products': products})

def send_userotp(request):
      global c_otp
      c_otp = randint(1000, 9999)
      sub = f"Email Verification Code : {c_otp}"
      message = f"Use This Code to finish setting up ypur account:\n{c_otp}\n\n This code will expire in 10 mins"
      from_email = settings.EMAIL_HOST_USER
      recipient_list = [user_data['email']]

      send_mail(sub, message, from_email, recipient_list)

# .............................User Authentication........................


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        try:
            Buyer.objects.get(email=request.POST['email'])
            return render(request, 'register.html', {"msg": 'Email Already in Use!!'})
        except:
            if request.POST['password'] == request.POST['cPassword']:
                global user_data
                user_data = {
                    'first_name': request.POST['first_name'],
                    'last_name': request.POST['last_name'],
                    'email': request.POST['email'],
                    'password': request.POST['password']
                }
                global c_otp
                c_otp = randint(1000, 9999)
                sub = f"Email Verification Code : {c_otp}"
                message = f"Use This Code to finish setting up ypur account:\n{c_otp}\n\n This code will expire in 10 mins"
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [user_data['email']]

                send_mail(sub, message, from_email, recipient_list)
                return render(request, 'verification.html', {'msg': "Enter Code Sent to Your Email."})

            else:
                return render(request, 'register.html', {'msg': 'Password does not match!!'})


def verification(request):
    if request.POST['u_otp'] == str(c_otp):
        Buyer.objects.create(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            password=user_data['password']
        )
        return render(request, 'login.html', {'msg': 'Congatulations !! Account Created Succesfully','task':'login'})
    else:
        return render(request, 'verification.html', {'msg': "Please Enter Correct OTP!!"})


def login(request):
    try:
      active(request)
      if request.method == "GET":
        return redirect('index')
    except:
        if request.method == "GET":
            return render(request, 'login.html',{'task':'login'})
        else:
                try:
                    user = Buyer.objects.get(email=request.POST['email'])
                    if user.password == request.POST['password']:
                            request.session['email'] = request.POST['email']
                            return redirect('index')
                    else:
                            return render(request, 'login.html', {'msg': 'Please Check the Password','task':'login'})
                except:
                    return render(request, 'login.html', {'msg': 'Email is not Registered','task':'login'})

def otp_login(request):
      if request.method == "GET":
            return render(request, 'login.html',{'task':'SEND OTP'})
      else:
            try:
                  global user_email
                  user = Buyer.objects.get(email = request.POST['email'])
                  user_email = request.POST['email']
                  global c_otp
                  c_otp = randint(1000, 9999)
                  sub = f"Email Verification Code : {c_otp}"
                  message = f"Use This Code to finish setting up ypur account:\n{c_otp}\n\n This code will expire in 10 mins"
                  from_email = settings.EMAIL_HOST_USER
                  recipient_list = [user_email]

                  send_mail(sub, message, from_email, recipient_list)
                  return render(request, 'login_verify.html', {'msg': "Enter Code Sent to Your Email."})
            except:
                  return render(request, 'login.html',{'task':'SEND OTP','msg':'User Do not Exist'})

def login_verify(request):
      if request.POST['u_otp'] == str(c_otp):
            request.session['email'] = user_email
            return redirect('index')
      else:
            return render(request, 'login_verify.html', {'msg': "Please Enter Correct OTP!!"})


def logout(request):
    del request.session['email']
    return redirect('index')


# ................................User Profile......................

def user_profile(request):
    active(request)
    return render(request, 'user_profile.html', {'active_user': active_user})


def edit_buyer(request):
    active(request)
    active_user.first_name = request.POST['first_name']
    active_user.last_name = request.POST['last_name']
    active_user.save()
    return redirect('user_profile')

def forgot_password(request):
    
    return redirect('user_profile')

def del_user(request):
    active(request)
    active_user.delete()
    return redirect(login)

# ...............................Cart Section..........................

razorpay_client = razorpay.Client(
auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def add_to_cart(request):
    try:
        pk = int(request.GET['id'])
        active(request)
        cartitems = Cart.objects.filter(buyer = active_user)
        cart1 = []
        for i in cartitems:
            cart1.append(i.product.id)
        if pk not in cart1: 
            Cart.objects.create(
                product=Product.objects.get(id=pk),
                buyer=active_user
            )
            return JsonResponse({'msg':'Added to Cart'})
        else:
            return JsonResponse({'msg':'Item Already in Cart'})
    except:
        return JsonResponse({'msg':'Login to Continue'})

def add(request,pk):
    cart_item=Cart.objects.get(id  = pk)
    product = Product.objects.get(id = cart_item.product.id)
    if product.product_stock >  cart_item.quantity:
        cart_item.quantity+=1
        cart_item.save()
    return redirect('cart')

def remove(request,pk):
    cart_item=Cart.objects.get(id  = pk)
    # product = Product.objects.get(id = cart_item.product.id)
    # product.product_stock += 1
    # product.save()
    if cart_item.quantity>0:
        cart_item.quantity-=1
        cart_item.save()
    return redirect('cart')

def delete_item(request):
    try:
        pk = request.GET['id']
        active(request)
        product = Cart.objects.get(id=pk)
        product.delete()    
        my_product = Cart.objects.filter(buyer = active_user)
        all_products = []
        global total_price 
        total_price = 0
        for i in my_product:
            total_price += (i.product.price*i.quantity)
            all_products.append({
                'pic' : i.product.product_pic.url,
                'name': i.product.product_name,
                'stock':i.product.product_stock,
                'price':i.product.price,
                'quantity':i.quantity,
                'id':i.id
            })

        if total_price > 0:  
            currency = 'INR'
            amount = total_price * 100  # Rs. 200
        
            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                            currency=currency,
                                                            payment_capture='0'))
        
            # order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            callback_url = 'paymenthandler/'
        
            # we need to pass these details to frontend.
            context = {}
            context['razorpay_order_id'] = razorpay_order_id
            context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            context['razorpay_amount'] = amount
            context['currency'] = currency
            context['callback_url'] = callback_url
            context['total_price'] = total_price
            context.update({'msg':"HEllo",'products' : all_products})
            return JsonResponse(context)
        else:
            return JsonResponse({'msg':"HEllo",'products' : all_products,'total_price':total_price})
    except:
        return JsonResponse({'msg':"Wrong"})

def cart(request):
    try:
        active(request)
        cart_items = Cart.objects.filter(buyer=active_user)
        global total_price
        total_price = 0
        for i in cart_items:
            total_price += (i.product.price*i.quantity)
            #...............................Payment Process...................
        if total_price > 0:  
            currency = 'INR'
            amount = total_price * 100  # Rs. 200
        
            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                            currency=currency,
                                                            payment_capture='0'))
        
            # order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            callback_url = 'paymenthandler/'
        
            # we need to pass these details to frontend.
            context = {}
            context['razorpay_order_id'] = razorpay_order_id
            context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            context['razorpay_amount'] = amount
            context['currency'] = currency
            context['callback_url'] = callback_url
            context['active_user'] = active_user
            context['cart_items'] = cart_items
            context['total_price'] = total_price
            return render(request, 'cart.html', context= context)
        else:
            return render(request, 'cart.html', {'active_user': active_user,'cart_items' : cart_items,'total_price': total_price})
    except:
        return redirect('login')


# ........................Payment Handle...................................
@csrf_exempt
def paymenthandler(request):
 
    # only accept POST request.
    if request.method == "POST":
        try:
           
        # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = total_price * 100 
                try:
                    active(request)
                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)
                    cart_items = Cart.objects.filter(buyer = active_user)
                    for i in cart_items:
                        MyOrder.objects.create(
                            buyer = active_user,
                            product = i.product,
                            quantity = i.quantity
                        )
                        product = Product.objects.get(id = i.product.id)
                        product.product_stock -= i.quantity
                        product.save()
                        i.delete()
                    # render success page on successful caputre of payment
                    return redirect('cart')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
 
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()

def myorder(request):
    active(request)
    orders  = MyOrder.objects.filter(buyer = active_user)
    total_price = 0
    for i in orders:
        total_price += i.product.price*i.quantity
    return render(request,'myorder.html',{'active_user':active_user,'orders' : orders,'total_price':total_price})


# ........................................EXTRAS.....................................

def about(request):
    try:
        active(request)
        return render(request, 'about.html', {'active_user': active_user})
    except:
        return render(request, 'about.html')


def care(request):
    try:
        active(request)
        return render(request, 'care.html', {'active_user': active_user})
    except:
        return render(request, 'care.html')


def codes(request):
    try:
        active(request)
        return render(request, 'codes.html', {'active_user': active_user})
    except:
        return render(request, 'codes.html')


def contact(request):
    try:
        active(request)
        return render(request, 'contact.html', {'active_user': active_user})
    except:
        return render(request, 'contact.html')


def faqs(request):
    try:
        active(request)
        return render(request, 'faqs.html', {'active_user': active_user})
    except:
        return render(request, 'faqs.html')


def hold(request):
    try:
        active(request)
        return render(request, 'hold.html', {'active_user': active_user})
    except:
        return render(request, 'hold.html')


def kitchen(request):
    try:
        active(request)
        return render(request, 'kitchen.html', {'active_user': active_user})
    except:
        return render(request, 'kitchen.html')


def offer(request):
    try:
        active(request)
        return render(request, 'offer.html', {'active_user': active_user})
    except:
        return render(request, 'offer.html')


def shipping(request):
    try:
        active(request)
        return render(request, 'shipping.html', {'active_user': active_user})
    except:
        return render(request, 'shipping.html')


def single(request):
    try:
        active(request)
        return render(request, 'single.html', {'active_user': active_user})
    except:
        return render(request, 'single.html')


def terms(request):
    try:
        active(request)
        return render(request, 'terms.html', {'active_user': active_user})
    except:
        return render(request, 'terms.html')


def wishlist(request):
    try:
        active(request)
        return render(request, 'wishlist.html', {'active_user': active_user})
    except:
        return render(request, 'wishlist.html')
