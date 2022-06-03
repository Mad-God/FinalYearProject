from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator 

# Create your models here.




class User(AbstractUser):
    pfp = models.ImageField(upload_to = 'static/users', blank = True, null = True)
    address = models.CharField(max_length=100, blank = True, null = True)
    phone = models.BigIntegerField(null = True, blank = True, unique = True)
    email = models.CharField(max_length=50, blank = True, null = True)


    
    def cart_items(self):
        cart_items = {}
        # print(cart_items[[str(a).split(" ")[0]] = a.quantity for a in self.cart.items.all()])
        for a in self.cart.items.all():
            cart_items[str(a).split(" ")[0]] = a.quantity
        print(cart_items)
        return cart_items
    def cart_prods(self):
        cart_items = []
        # print(cart_items[[str(a).split(" ")[0]] = a.quantity for a in self.cart.items.all()])
        for a in self.cart.items.all():
            cart_items.append(a.product)
        print(cart_items)
        return cart_items


class Shop(models.Model):
    cat_choices = (
        ('General', 'GEN'),
        ('Dairy', 'DRY'),
        ('Bakery', 'BKR'),
    )

    name = models.CharField(max_length=50)
    pfp = models.ImageField(upload_to = 'static/shops', blank = True, null = True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null = True, blank = True, related_name = "shop")
    category = models.CharField(choices = cat_choices,max_length= 100)
    
    open_time = models.TimeField()
    close_time = models.TimeField()
    phone = models.BigIntegerField(null = True, blank = True, unique = True)
    email = models.EmailField(null = True, blank = True, unique = True)

    address = models.CharField(max_length=200, null=True, blank=True) 

    rzp_pr_key = models.CharField(max_length=400, default = "omFNDCkZBgjorzpFzNNmfKyd") 
    rzp_pb_key = models.CharField(max_length=400, default = "rzp_test_0ovBWEVK2aFRht")


    def __str__(self):
        return self.name



class Notifications(models.Model):
    description = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank = True, null = True)


