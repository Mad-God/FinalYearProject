from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import (
                        ProductModelForm, ProductStockUpdateForm, 
                        CategoryModelForm, ItemModelForm, OrderModelForm, OrderModelForm2, 
                        OrderUpdateModelForm, StockUpdateForm
                    )
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Shop
from .models import Product, Category, OrderItem, Order, Cart, StockFile, Item
import razorpay
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import os
import hashlib


# Create your views here.


class ShopView(ListView):
    template_name = 'shop/product_list.html'




class ProductListView(ListView):    
    template_name = 'shop/product_list.html'
    def get_queryset(self, **kwargs):
        category = self.kwargs['cat']
        print(Product.objects.filter(shop__pk = self.kwargs['pk']))
        if self.kwargs['cat'] == 0:
            queryset = Product.objects.filter(shop__pk = self.kwargs['pk'])
        # queryset.filter(category = category)
        else:
            category_item = Category.objects.get(id = category)
            queryset = Product.objects.filter(shop__pk = self.kwargs['pk'])
            queryset = queryset.filter(category = category_item)
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        shop = Shop.objects.get(id = self.kwargs['pk'])
        form = ProductStockUpdateForm()
        selected_cat_id = self.kwargs["cat"]
        if selected_cat_id != 0:
            curr_category = Category.objects.get(id = selected_cat_id)
            print("asds: ",curr_category)
        else:
            curr_category = "All"
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(shop = shop)
        orders = orders.filter(completed = False).count()
        categories = Category.objects.filter(shop = shop)
        cart_items = self.request.user.cart_items()
        print("cart_items:", cart_items)

        cart_p = self.request.user.cart_prods()
        print("cart_prods:", cart_p)
        p_ids = [x.id for x in cart_p ]
        print(p_ids)
        prods = Product.objects.filter(pk__in=p_ids)
        cart = Item.objects.filter(cart=self.request.user.cart)
        # for i in cart_items:
        #     print(i)
        #     cart_p.append(i.product)
        context.update({
            'shop':shop,
            "form":form,
            "categories":categories,
            "current_category":curr_category,
            "cart_items": cart,
            "prods":prods,
            "orders": orders
        })

        


        return context
          


class CreateCategoryView(ListView):
    template_name = "shop/category_list.html"
    def get_queryset(self):
        shop = Shop.objects.get(id = self.kwargs['pk'])
        return Category.objects.filter(shop = shop)



class ProductCreateView(CreateView):
    template_name = 'shop/product_create.html'
    form_class = ProductModelForm
    def get_success_url(self):
        # print(self.kwargs['id'])
        # print(self.request.pk)
        # print(self.request.id)
        # print(self.request.shop.id)
        # prod = self.kwargs['id']
        print(self.kwargs)
        return reverse('shop:home', kwargs = {'pk': self.object.shop.id, 'cat':0})
        # , kwargs = {'pk': prod})
    # to send an email when a new lead is created
    def form_valid(self, form):
        # do whatever u want to do here
        prod = form.save(commit=False)
        shop_id = self.kwargs['pk']
        # print(self)
        # prod.shop = Shop.objects.get(id = shop_id)
        prod.shop = self.request.user.shop
        print(self.kwargs['pk'])
        # print(self.get_object())
        
        prod.save()
        return super(ProductCreateView, self).form_valid(form)
    def get_form_kwargs(self):
        kwargs = super(ProductCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs



class ProductDeleteView(DeleteView):
    def get_queryset(self):
        prod_id = self.kwargs['pk']
        print(prod_id)
        prod = Product.objects.get(id = prod_id)
        queryset = Product.objects.filter(shop = prod.shop)
        return queryset

    template_name = 'shop/product_delete.html'
    def get_success_url(self):
        prod = self.get_object()
        return reverse("shop:home", kwargs = {'pk':prod.shop.id, "cat":0})



class ProductUpdateView(UpdateView):
    template_name = 'shop/product_update.html'
    form_class = ProductStockUpdateForm

    
    def get_context_data(self, **kwargs):
        curr_prod = Product.objects.get(id = self.kwargs["pk"])
        form = ProductStockUpdateForm(instance = curr_prod)
        prod_id = self.kwargs['pk']
        
        prod = Product.objects.get(id = prod_id)
        # print(prod)
        queryset = Product.objects.get(id = prod_id)
        context = super().get_context_data(**kwargs)
        context.update({
            'prod':prod,
            'categories':prod.get_categories()
        })
        return context
    
    
    def get_queryset(self): 
        user = self.request.user
        queryset = user.shop.products.all()
        return queryset

    
    def get_success_url(self):
        return reverse('shop:product_update', kwargs = {'pk': self.kwargs['pk']})





# normal view for create
def category_create(request, pk):
    msg = ''
    form = CategoryModelForm()
    if request.method == 'POST':
        form = CategoryModelForm(request.POST)
        if form.is_valid():
            cat = form.save(commit = False)
            shop = Shop.objects.get(id = pk)
            cat.shop = shop
            cat.save()
            return redirect('shop:categories', pk = pk)

        else:
            print('\n\nForm Invalid!!!')
    shop = Shop.objects.get(id = pk)
    categories = Category.objects.filter(shop = shop)
    context = {'form':form, 'msg':msg, 'categories': categories}
    return render(request , 'shop/category_list.html', context)



def category_delete(req, pk):
    lead = Category.objects.get(id = pk)
    shop = lead.shop
    lead.delete()
    return redirect("shop:categories", pk = shop.id)



class ItemCreateView(CreateView):
    template_name = 'shop/item_create.html'
    form_class = ItemModelForm
    def get_success_url(self):
        print(self.object.product.shop)
        print("asdsadasd")

        return reverse('shop:home', kwargs = {'pk': self.object.product.shop.id, 'cat':0})
        
    def form_valid(self, form):
        prod = form.save(commit=False)
        product_id = self.kwargs['pk']
        prod.product = Product.objects.get(id = product_id)
        prod.cart = self.request.user.cart
        prod.save()
        return super(ItemCreateView, self).form_valid(form)




def StockUpdateView(request, pk):
    msg = ''
    instance = request.user.shop.stockfile.last()
    # try:
    form = StockUpdateForm(instance = instance)
    # except:
    #     form = StockUpdateForm()
    if request.method == 'POST':
        form = StockUpdateForm(data = request.POST, files = request.FILES)
        print(form.errors)
        if form.is_valid():
            instance = request.user.shop.stockfile.last()
            print(str(instance.stock_file))
            if os.path.exists(str(instance.stock_file)):
                print(str(instance.stock_file))
                print("removed above file")
                os.remove(str(instance.stock_file))
            else:
                print("couldn't find  the file: " , str(instance.stock_file))
            
            cat = form.save(commit = False)
            print(cat)
            cat.shop = request.user.shop
            print(form.cleaned_data.get('stock_id'))
            print(cat.stock_file)
            cat.save()
            print(cat.stock_file)
            file_stock = cat.stock_file
            # sf = pd.read_excel(f"shop/static/stockfiles/{cat.stock_file}", sheet_name=cat.stock_file)
            # sf = pd.read_excel(f"shop/static/stockfiles/{file_stock}", header =1)
            sf = pd.read_excel(cat.stock_file, header =1)
            # print(sf)
            for i in range(0,20):
                # print(sf.iloc[i,:])
                prd = sf.iloc[i,:]
                print(prd["Code"])
                if Product.objects.filter(code = prd["Code"]).exists():
                    prod = Product.objects.get(code = prd["Code"])
                    prod.stock = prd[cat.stock_column_name]
                    print("\n\n\nupdating objects.")
                    stock = int(prd[cat.stock_column_name])
                    stock = stock if stock < 0 else stock * (-1)
                    print("stokc in line: ", stock)
                    if stock < 0:
                        stock *= -1
                        print("stokc in if: ", stock)
                    print("stokc outside ifs: ", stock)
                    price = int(prd[cat.price_column_name])
                    price = price if price < 0 else price * (-1)
                    print("price after single line: ",price)
                    if price < 0:
                        price *= -1
                        print("type of price: ", type(price))
                        print("type of price: ", type(20))
                        print("price in if: ",price)
                    print("stock :",stock)
                    print("price :",price )\
                    # prod.stock = prd[cat.stoc_column_name]
                    print("updated objects: ", prod)
                    prod.price = price
                    prod.stock = stock
                    print("updated objects: ", prod)
                    prod.save()

                else:
                    code = prd["Code"]
                    name = prd[cat.name_column_name]
                    stock = int(prd[cat.stock_column_name])
                    stock = stock if stock < 0 else stock * (-1)
                    print("stokc in line: ", stock)
                    if stock < 0:
                        stock *= -1
                        print("stokc in if: ", stock)
                    print("stokc outside ifs: ", stock)
                    price = int(prd[cat.price_column_name])
                    price = price if price < 0 else price * (-1)
                    print("price after single line: ",price)
                    if price < 0:
                        price *= -1
                        print("type of price: ", type(price))
                        print("type of price: ", type(20))
                        print("price in if: ",price)
                    shop = request.user.shop
                    print("code :", code)
                    print("name :",name )
                    print("stock :",stock if stock < 0 else stock * (-1) )
                    print("price :",price )
                    print("shop :",shop )
                    Product.objects.create(code = code,
                                            name = name,
                                            stock = stock,
                                            price = price,
                                            shop = request.user.shop,
                                            )
                # print(it)

            # shop = Shop.objects.get(id = pk)
            # cat.shop = shop
            # cat.save()
            return redirect('shop:stock-update',request.user.shop.id)

        else:
            print('\n\nForm Invalid!!!')
    shop = Shop.objects.get(id = pk)
    categories = list(x.name for x in Category.objects.filter(shop = shop))
    context = {'form':form, 'msg':msg, 'categories': categories, 'shop':shop}
    return render(request , 'shop/stock_update.html', context)





class ItemUpdateView(UpdateView):
    template_name = 'shop/item_update.html'
    form_class = ItemModelForm
    def get_success_url(self):
        print(self.object.product.shop)
        print("asdsadasd")

        return reverse('shop:home', kwargs = {'pk': self.object.product.shop.id, 'cat':0})

    def get_queryset(self):
        queryset = self.request.user.cart.items.all()
        print(queryset)
        return queryset
        
    


    def form_valid(self, form):
        prod = form.save(commit=False)
        # product_id = self.kwargs['pk']
        # prod.product = Product.objects.get(id = product_id)
        # prod.cart = self.request.user.cart
        prod.save()
        return super(ItemUpdateView, self).form_valid(form)




class CheckoutDetailView(ListView):
    template_name = "base/checkout.html"
    # context_object_name = "items"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total = 0
        shop = Shop.objects.get(id = self.kwargs['pk'])
        for item in self.object_list:
            print(item.product.price * item.quantity)
            total += item.product.price * item.quantity
        
        context.update({
            'shop_current':shop,
            'total':total
        })
        return context

    def get_queryset(self):
        user = self.request.user
        cart = Cart.objects.get(user = user)
        print(user)
        print(cart)
        shop = Shop.objects.get(id = self.kwargs["pk"])
        print(shop)
        # queryset = Item.objects.filter(cart = cart)
        queryset = self.request.user.cart.items.filter(product__shop = shop)
        print(queryset)
        # queryset = queryset.filter(shop = self.get_object())
        # for item in queryset:
        #     print(items)
        return queryset
    



class OrderCreateView(CreateView):
    template_name = 'shop/order_create.html'
    form_class = OrderModelForm
    def get_success_url(self):
        order = self.request.user.order.last()
        print(order)
        print("Order created. Check for COD.")
        if order.cash_on_pickup == True:
            return reverse('cart', kwargs = {'pk': self.request.user.id})
        else:
            return reverse('payment', kwargs = {'pk':order.id})

    def form_valid(self, form):
        order = form.save(commit=False)

        shop = Shop.objects.get(id = self.kwargs['pk'])
        items = self.request.user.cart.items.filter(product__shop = shop)

        order.shop = shop
        order.user = self.request.user
        print("asdasdas\n\n\n")
        total = 0
        for item in items:
            # OrderItem.objects.create(order = )
            print(item.product.price * item.quantity)
            total += item.product.price * item.quantity
        order.price = total
        order.completed = False
        print(order)

        order.save()

        return super(OrderCreateView, self).form_valid(form)


    def get_context_data(self, **kwargs):
        form = OrderModelForm(initial = {'address': self.request.user.address})
        context = super().get_context_data(**kwargs)
        context.update({
            'form':form,
            "shop":self.kwargs["pk"]
        })
        return context




class OrderListCustomerView(ListView):
    template_name = 'shop/order_list_customer.html'
    def get_queryset(self, **kwargs):
        customer = self.request.user

        orders = Order.objects.filter(user=customer)
        unfinished_orders = orders.filter(completed = False)
        finished_orders = orders.filter(completed = True)
        return orders

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(user = self.request.user)
        unfinished_orders = orders.filter(completed = False)
        finished_orders = orders.filter(completed = True)

        context.update({
            "orders": orders,
            'unfinished':unfinished_orders,
            'finished':finished_orders,
        })
        return context




class OrderListView(ListView):
    template_name = 'shop/order_list.html'
    def get_queryset(self, **kwargs):
        shop_id = self.kwargs['pk']
        shop = Shop.objects.get(id = shop_id)

        orders = Order.objects.filter(shop=shop)
        unfinished_orders = orders.filter(completed = False)
        finished_orders = orders.filter(completed = True)
        return orders

    def get_context_data(self, **kwargs):
        shop = Shop.objects.get(id = self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(shop = shop)
        unfinished_orders = orders.filter(completed = False)
        finished_orders = orders.filter(completed = True)

        context.update({
            'shop':shop,
            "orders": orders,
            'unfinished':unfinished_orders,
            'finished':finished_orders,
        })
        return context




class OrderUpdateView(UpdateView):
    template_name = 'shop/order_update.html'
    form_class = OrderUpdateModelForm
    def get_success_url(self):
        # print(self.object.product.shop)
        # print("asdsadasd")

        return reverse('shop:order-list', kwargs = {'pk': self.object.shop.id})

    def get_queryset(self):
        queryset =Order.objects.filter(id=self.kwargs['pk'])
        print("inside  get_queryset()")
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("order:id = ", self.kwargs["pk"])
        order_id = self.kwargs['pk']
        order = Order.objects.get(id = order_id)
        items = OrderItem.objects.filter(order = order)
        context.update({
            "items":items,
            "user":order.user,
            "order":order
        })
        return context
    
         


def payment_handler(request, pk,  **kwargs):
    print("kwargs in payment_handler: ",kwargs)
    # order = Order.objects.get(id = pk)
    shop = Shop.objects.get(id = pk)
    print(shop)
    items = request.user.cart.items.filter(product__shop = shop)
    print(items)
    total = 0
    for item in items:
        # OrderItem.objects.create(order = )
        print(item.product.price * item.quantity)
        total += item.product.price * item.quantity
    
    # if request.method == "POST":
    client = razorpay.Client(auth=("rzp_test_0ovBWEVK2aFRht", "omFNDCkZBgjorzpFzNNmfKyd"))
    amount = total * 100
    order_currency = 'INR'
    print("in the form post")
    print(request.POST.get("razorpay_signature") or "jhfjgv")
    print(request.POST.get)
    order_id = request.POST.get("razorpay_payment_id")
    print("end of post.\n")
        # generated_signature = hashlib.sha256(str(order.id) + "|" + order_id , "omFNDCkZBgjorzpFzNNmfKyd")

        # if (generated_signature == razorpay_signature):
        #     print("payment is successful")
        
        # payment = client.order.create()
    DATA = {
        "amount": amount,
        "currency": "INR",
        'payment_capture':'1',
    }
    payment = client.order.create(data=DATA)
    form = OrderModelForm2()
    return render(request, "shop/payment4.html", {"cart":items, "payment":payment, "form": form, "shop":shop, "total":total})




def payment_handler_with_order_id(request, pk):
    print(pk)
    amount = 500
    order_currency = 'INR'
    client = razorpay.Client(auth=("rzp_test_0ovBWEVK2aFRht", "omFNDCkZBgjorzpFzNNmfKyd"))
    
    order = Order.objects.get(id = pk)
    # payment = client.order.create()
    DATA = {
        "amount": order.price * 100,
        "currency": "INR",
        'payment_capture':'1',
    }

    payment = client.order.create(data=DATA)

    # print(order.price)
    print(payment)
    print(payment["id"])
    print(payment)


    if request.method == "POST":
        print("\n\npayment done.")
        # params_dict = {'razorpay_order_id': payment['order_id'],'razorpay_payment_id': '332','razorpay_signature': '23233'}
        print(payment)
        print(order.order_id)
        # client.utility.verify_payment_signature(params_dict)
        print(client)
        try:
            print(client.order.payment(payment["id"]))
        except:
            print("client.order.payment(payment[id])  failed")
        try:
            print(client.order.payment.fetch(payment["id"]))
        except:
            print("client.order.payment.fetch(payment[id]) failed")
            
        try:
            print(payment.order.payment(payment["id"]))
        except:
            print("payment.order.payment(payment[id]) failed")
        try:
            print(payment.order.payment.fetch(payment["id"]))
        except:
            print("payment.order.payment.fetch(payment[id]) failed")
        print("Payment done.")
    return render(request, "shop/payment.html", {"order":order, 'payment':payment})




@csrf_exempt
def success(request):
    if request.method == "POST":
        order = form.save(commit=False)

        shop = Shop.objects.get(id = self.kwargs['pk'])
        items = self.request.user.cart.items.filter(product__shop = shop)

        order.shop = shop
        order.user = self.request.user
        print("asdasdas\n\n\n")
        total = 0
        for item in items:
            # OrderItem.objects.create(order = )
            print(item.product.price * item.quantity)
            total += item.product.price * item.quantity
        order.price = total
        order.completed = False
        print(order)

        order.save()

        return super(OrderCreateView, self).form_valid(form)
        if not request.POST.get("cod"):
            print(request.POST.get("razorpay_signature") or "Got nothing")
            print(request.POST.get("razorpay_payment_id") or "Got nothing")
            print(request.POST.get("razorpay_order_id") or "Got nothing")
            
            client = razorpay.Client(auth=("rzp_test_0ovBWEVK2aFRht", "omFNDCkZBgjorzpFzNNmfKyd"))
            params_dict = {
                'razorpay_signature': request.POST.get("razorpay_signature"),
                'razorpay_payment_id': request.POST.get("razorpay_payment_id"),
                'razorpay_order_id': request.POST.get("razorpay_order_id")
            }
            succ = client.utility.verify_payment_signature(params_dict)
            order = Order.objects.get(id = int(request.POST.get("order_id")))
            print(succ)
            if not succ:
                # return HttpResponse("Payment Failed.")
                return redirect("payment",pk = order.id)
            print(request.POST.get("order_id"))
            order.is_paid = True
            order.signature = request.POST.get("razorpay_signature")
            order.order_id = request.POST.get("razorpay_order_id")
            order.payment_id = request.POST.get("razorpay_payment_id")
            order.save()
        else:
            print("the order is to be created")
        # except:
        #     print("Failed in success()")
    return render(request, "shop/payment_success.html")