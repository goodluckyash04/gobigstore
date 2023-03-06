
from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),

    path('register/',register,name='register'),
    path('verification/',verification,name='verification'),
    path('login/',login,name='login'),
    path('otp_login/',otp_login,name='otp_login'),
    path('login_verify/',login_verify,name='login_verify'),
    path('logout/',logout,name='logout'),

    path('user_profile/',user_profile,name='user_profile'),
    path("edit_buyer/",edit_buyer, name="edit_buyer"),
    path("forgot_password/",forgot_password, name="forgot_password"),
    path('del_user/',del_user,name='del_user'),

    path('cart/',cart,name='cart'),
    path('cart/paymenthandler/', paymenthandler, name='paymenthandler'),
    path('addtocart/',add_to_cart,name='add_to_cart'),
    path('add/<int:pk>',add,name='add'),
    path('remove/<int:pk>',remove,name='remove'),
    path('delete_item/',delete_item,name='delete_item'),

    path('myorder/',myorder,name='myorder'),

    path('about/',about,name='about'),
    path('care/',care,name='care'),
    path('codes/',codes,name='codes'),
    path('contact/',contact,name='contact'),
    path('faqs/',faqs,name='faqs'),
    path('hold/',hold,name='hold'),
    path('kitchen/',kitchen,name='kitchen'),
    path('offer/',offer,name='offer'),
    path('shipping/',shipping,name='shipping'),
    path('single/',single,name='single'),
    path('terms/',terms,name='terms'),
    path('wishlist/',wishlist,name='wishlist')
]


# path('add_user/',add_user,name='add_user'),
    # 