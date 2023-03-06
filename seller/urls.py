from django.urls import path
from .views import *

urlpatterns = [
    path('', seller_index, name='seller_index'),
    path('login/', seller_login, name='seller_login'),
    path('register/', seller_register, name='seller_register'),
    path('verification/', seller_verification, name='seller_verification'),
    path('resendotp/',resend_otp,name='resend_otp'),
    path('edit_details/', edit_details, name='edit_details'),
    path('profile/', profile, name='profile'),
    path('logout/', seller_logout, name='seller_logout'),
    path('add_product/', add_product, name='add_product'),
    path('products/', products, name='products'),
    path('edit_product/<int:pk>', edit_product, name='edit_product'),
    path('delete_product/<int:pk>', delete_product, name='delete_product'),
    path('recent_order/', recent_order, name='recent_order'),
    path('completed_order/', completed_order, name='completed_order'),
    path('dispatch/<int:pk>', dispatch, name='dispatch'),
    path('charts/', charts, name='charts'),
    path('map/', map, name='map') 
]


# path('add_user/',add_user,name='add_user'),
# path('del_user/',del_user,name='del_user')
