from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete
from django.dispatch import receiver
from base.models import Shop, User
from datetime import datetime

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length = 25, )
    shop = models.ForeignKey(Shop, related_name = "categories", on_delete = models.CASCADE, null = True, blank = True, )
    
    class Meta:
        unique_together = ("name", "shop")
    
    def __str__(self):
        return self.name






class Supplier(models.Model):
    name = models.CharField(max_length = 25, )
    shop = models.ForeignKey(Shop, related_name = "suppliers", on_delete = models.CASCADE, null = True, blank = True, )

    address = models.CharField(max_length=40, blank = True, null = True)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=40, blank = True, null = True)

    
    class Meta:
        unique_together = ("name", "shop")
    

    def __str__(self):
        return self.name







class Slide(models.Model):
    text = models.CharField(max_length = 40)
    user = models.ForeignKey(User, related_name = "slides", on_delete = models.CASCADE)
    img = models.ImageField(upload_to = 'static/slides', blank = True, null = True)

    def __str__(self):
        return self.text[:10] + " - from: " + str(self.user)





class StockFile(models.Model):
    price_column_name = models.CharField(max_length  = 40)
    stock_column_name = models.CharField(max_length  = 40)
    name_column_name = models.CharField(max_length  = 40)
    stock_file = models.FileField(upload_to='shop/static/stockfiles')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank = True, related_name = "stockfile")
    code_column_name = models.CharField(max_length  = 40, null=True, blank = True)



class Product(models.Model):

    # supplier = models.CharField(choices = suppliers,max_length= 100, null = True, blank = True)
    supplier = models.ForeignKey(Supplier, related_name = "products", null = True, blank = True, on_delete = models.SET_NULL)
    name = models.CharField(max_length=50)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    code = models.IntegerField(blank = True, null=True, default = -1)
    category = models.ManyToManyField(Category, related_name = "products",null = True, blank = True, )
    index = models.CharField(max_length=100, null = True, blank = True, )
    img = models.ImageField(upload_to = 'static/products', blank = True, null = True)

    
    class Meta:
        unique_together = ("name", "shop")
    


    def get_categories(self):
        print(', '.join([str(a) for a in self.category.all()]))
        return ', '.join([str(a) for a in self.category.all()])
        # return "all Categories here."
    def __str__(self):
        return self.name




class Item(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, null=True, blank = True, related_name = "items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank = True, related_name = "items")
    quantity = models.PositiveIntegerField(default = 1)
    def __str__(self):
        return self.product.name + " for " + str(self.cart)




class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "cart", null=True, blank = True)
    def __str__(self):
        return self.user.username + "'s cart"




class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete = models.CASCADE, related_name = 'orderItems')
    # item = models.ForeignKey("Item", on_delete = models.CASCADE, related_name = 'orderItems')
    cart = models.ForeignKey("Cart", on_delete=models.CASCADE, null=True, blank = True, related_name = "orderItems")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank = True, related_name = "orderItems")
    quantity = models.PositiveIntegerField(default = 1)
    def __str__(self):
        return str(self.product) + " ordered"




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'order')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name = 'order')
    price = models.PositiveIntegerField()
    completed = models.BooleanField(default = False)
    order_time = models.DateTimeField(default = datetime.now, blank = True)
    complete_time = models.DateTimeField(blank = True, null = True)
    # cash_on_delivery = 
    address = models.CharField(max_length = 100, null = True, blank = True)
    instruction = models.CharField(max_length = 200, null = True, blank = True)
    delivery = models.BooleanField(default = False)
    cash_on_pickup = models.BooleanField(default = False)
    accepted = models.BooleanField(default = False)
    def __str__(self):
        return "For " + str(self.user) + " from " + str(self.shop) + " on " + str(self.order_time)
    
    signature = models.CharField(max_length = 100, null = True, blank = True)
    payment_id = models.CharField(max_length = 100, null = True, blank = True)
    order_id = models.CharField(max_length = 100, null = True, blank = True)
    is_paid = models.BooleanField(default = False)




# @receiver(post_save, sender = User)
def post_user_created_signal(sender, instance, created, **kwargs):
    print(instance, created)
    if created:
        Cart.objects.create(user = instance)




def post_order_created_signal(sender, instance, created, **kwargs):
    if created:
        print(instance, created)
        print("Printed from the signal. New.")
        items = instance.user.cart.items.filter(product__shop = instance.shop)

        print(items)
        for item in items:
            # OrderItem.objects.create(order = instance, item = item)
            order = OrderItem(order = instance, product = item.product, cart = item.cart, quantity = item.quantity)
            order.save()

            total = item.product.price * item.quantity
            prod = item.product
            prod.stock -= item.quantity
            print("\n\n\n",prod,"\n\n\n")
            prod.save()
            item.delete()



def post_orderItem_created_signal(sender, instance, created, **kwargs):
    if created:
        print("Order item created:", instance)




def order_delete_signal(sender, instance, *args,  **kwargs ):
    print("kwargs: ", kwargs)
    print("args: ", args)
    print(instance)
    orditm = OrderItem.objects.filter(order = instance)

    for oi in orditm:
        print(oi)
        cart = oi.cart
        quan = oi.quantity
        prod = oi.product
        prod.stock += quan
        prod.save()
        # Items.objects.create(cart = cart, quantity = quan, product = prod)
       





post_save.connect(post_order_created_signal, sender = Order)


post_save.connect(post_user_created_signal, sender = User)


post_save.connect(post_orderItem_created_signal, sender = OrderItem)


pre_delete.connect(order_delete_signal, sender = Order)





