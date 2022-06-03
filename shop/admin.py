from django.contrib import admin
from .models import Product, Category, Item, Cart, Order, OrderItem, StockFile, Slide, Supplier

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(StockFile)
admin.site.register(Supplier)
admin.site.register(Slide)