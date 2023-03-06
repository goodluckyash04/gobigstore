from django.db import models
from seller.models import *

# Create your models here.

# orm object Relational mapping.
# class is table , variable is columnes and object is rows.

# python manage.py makemigrations
# python manage.py migrate

class Buyer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    address = models.TextField(max_length=250)

    def __str__(self):
        return self.email

class Cart(models.Model):
    product =  models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer =  models.ForeignKey(Buyer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.product_name