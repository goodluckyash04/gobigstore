from django.db import models

# Create your models here.
class Seller(models.Model):
    shop_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    gst_no = models.CharField(max_length=15)
    profile_pic = models.FileField(upload_to='profile_pics',default="default.png")
    
    def __str__(self):
        return self.shop_name

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    price = models.FloatField(default=1.0)
    product_stock = models.IntegerField(default=0)
    product_pic = models.FileField(upload_to='product_pics', default='productdef.png')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

class MyOrder(models.Model):
    current_status = [
        ("P", 'pending'),
        ("D", 'dispatched')
    ]
    buyer =  models.ForeignKey(to='buyer.Buyer', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date = models.DateField( auto_now_add=True)
    status = models.CharField(max_length=50,choices=current_status,default="P")

    def __str__(self):
        return self.product.product_name

# python manage.py makemigrations
# python manage.py migrate
