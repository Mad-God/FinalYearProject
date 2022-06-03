from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import (
                        ProductModelForm, ProductStockUpdateForm, 
                        CategoryModelForm, ItemModelForm, OrderModelForm, 
                        OrderUpdateModelForm, StockUpdateForm,
                        SlideModelForm, SupplierModelForm, SupplierUpdateForm,
                    )
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Shop, User
from .models import Product, Category, OrderItem, Order, Cart, StockFile, Item, Slide, Supplier
import razorpay
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import os
from base.forms import ShopUpdateForm, ShopCreateForm, ConfirmUserForm, UpdateBankDetailsForm
from django.db.models import Sum



from django.core.paginator import Paginator
import folium
import geocoder as gc
from django.contrib.auth.models import auth
from cryptography.fernet import Fernet
# Create your views here.



encryption_key = b"zdeU8DTcUCwtACFlKKwh1lGMOq1i6wd3YmOFduJsfbk="
encrypter = Fernet(encryption_key)


# ******************* SHOP VIEWS ********************


class ShopUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'shop/shop/shop_update.html'
    form_class = ShopUpdateForm
    def get_success_url(self):
        # print(self.object.product.shop)
        # print("asdsadasd")

        return reverse('shop:shop-update', kwargs = {'pk': self.request.user.shop.id})

    def get_queryset(self):
        queryset =Shop.objects.filter(id=self.kwargs['pk'])
        print("inside  get_queryset()")
        print(queryset)
        return queryset
    
    def get_context_data(self, **kwargs):
        shop = Shop.objects.get(id = self.kwargs['pk'])
        form = ShopUpdateForm(instance = shop)
        orders = Order.objects.filter(shop=shop)
        total_sales = Order.objects.filter(shop=shop).aggregate(Sum('price'))
        context = super().get_context_data(**kwargs)
        context.update({
            'shop':shop,
            "form":form,
            "total_sales":total_sales["price__sum"] if total_sales["price__sum"] else 0,
            "order_num":len(orders)
        })
        
        return context
    

class ShopCreateView(LoginRequiredMixin, CreateView):
    template_name = 'shop/shop/shop_create.html'
    form_class = ShopCreateForm
    def get_success_url(self):
        print(self.kwargs) 
        return reverse('shop:home', kwargs = {'pk': self.object.id, 'cat':0})

    def form_valid(self, form):
        shop = form.save(commit=False)
        shop.user = self.request.user
        # print(self.kwargs['pk'])
        pbk = shop.rzp_pb_key
        pbk = encrypter.encrypt(pbk.encode())
        shop.rzp_pb_key = pbk

        prk = shop.rzp_pr_key
        prk = encrypter.encrypt(prk.encode())
        shop.rzp_pr_key = prk

        shop.save()
        return super(ShopCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ShopCreateView, self).get_form_kwargs()
        # kwargs.update({'user': self.request.user})
        return kwargs



class ShopView(LoginRequiredMixin, ListView):
    template_name = 'shop/product_list.html'


def confirm_user_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = None
        user = auth.authenticate(username = username, password = password)
        if user:
            if user==request.user:
                return redirect("shop:update-bank", pk=request.user.shop.id)
            else:
                return HttpResponse("You are not the owner of this shop. Please go back and login as the owner.")
        else:
            return HttpResponse("Authentication Failed. Please go back and try again.")


    else:
        form = ConfirmUserForm()
        return render(request, "shop/shop/confirm_user.html", {"form":form})



class BankDetailUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'shop/shop/update_bank_details.html'
    form_class = UpdateBankDetailsForm
    def get_success_url(self):
        # print(self.object.product.shop)
        # print("asdsadasd")

        return reverse('shop:shop-update', kwargs = {'pk': self.request.user.shop.id})

    def get_queryset(self):
        queryset =Shop.objects.filter(id=self.kwargs['pk'])
        print("inside  get_queryset()")
        print(queryset)
        return queryset
    
    def get_context_data(self, **kwargs):
        shop = Shop.objects.get(id = self.kwargs['pk'])
        form = UpdateBankDetailsForm(instance = shop)
        context = super().get_context_data(**kwargs)
        context.update({
            'shop':shop,
            "form":form,
        })
        return context
    
    
    def form_valid(self, form):
        shop = form.save(commit=False)
        shop.user = self.request.user
        # print(self.kwargs['pk'])
        pbk = shop.rzp_pb_key
        pbk = encrypter.encrypt(pbk.encode())
        shop.rzp_pb_key = pbk

        prk = shop.rzp_pr_key
        prk = encrypter.encrypt(prk.encode())
        shop.rzp_pr_key = prk

        shop.save()
        return super(BankDetailUpdateView, self).form_valid(form)


    



# ******************** PRODUCT VIEWS ****************



class ProductListView(LoginRequiredMixin, ListView):    
    template_name = 'shop/product_list.html'

    def form_valid(self):
        print("\n\n\n\n\nasdkjasdbjhabsdjhbasd\n\n\n\n")
        if self.request.POST.get("q"):
            print("\n\n\n\n",self.request.POST.get("q"))


    def get_queryset(self, **kwargs):
        category = self.kwargs['cat']

        # print(Product.objects.filter(shop__pk = self.kwargs['pk']))
        # queryset.filter(category = category)
        if self.kwargs['cat'] == 0:
            queryset = Product.objects.filter(shop__pk = self.kwargs['pk'])
        else:
            category_item = Category.objects.get(id = category)
            queryset = Product.objects.filter(shop__pk = self.kwargs['pk'])
            queryset = queryset.filter(category = category_item)
        # print(queryset)
        
        
        if self.request.GET.get("q"):
            print("\n\n\n\n",self.request.GET.get("q"), "get")
            queryset = queryset.filter(name__icontains = self.request.GET.get("q"))
            q2 = Product.objects.filter(index__icontains = self.request.GET.get("q"), shop__pk = self.kwargs['pk'])
            print(q2)
            print("final qs: ", queryset)
            queryset = queryset.union(q2)
        # pagination
        p = Paginator(queryset, 10)
        page = self.request.GET.get("page")
        qs = p.get_page(page)

        return qs

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
        # print("cart_items:", cart_items)

        cart_p = self.request.user.cart_prods()
        # print("cart_prods:", cart_p)
        p_ids = [x.id for x in cart_p ]
        # print(p_ids)
        prods = Product.objects.filter(pk__in=p_ids)

        slides = Slide.objects.filter(user = shop.user)

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
            "orders": orders,
            "slides":slides,
        })

        


        return context
          



class ProductListWholeView(LoginRequiredMixin, ListView):    
    template_name = 'shop/product_list_whole.html'

    def form_valid(self):
        print("\n\n\n\n\nasdkjasdbjhabsdjhbasd\n\n\n\n")
        if self.request.POST.get("q"):
            print("\n\n\n\n",self.request.POST.get("q"))


    def get_queryset(self, **kwargs):
        # category = self.kwargs['cat']

        # print(Product.objects.filter(shop__pk = self.kwargs['pk']))
        # queryset.filter(category = category)
        # if self.kwargs['cat'] == 0:
        #     queryset = Product.objects.filter(shop__pk = self.kwargs['pk'])
        # else:
        #     category_item = Category.objects.get(id = category)
        #     queryset = Product.objects.filter(shop__pk = self.kwargs['pk'])
        #     queryset = queryset.filter(category = category_item)
        # print(queryset)
        queryset = Product.objects.all()
        print("get request data", self.request.GET)
        print("post request data", self.request.POST)
        print("kwargs request data", kwargs)
        print("full path request data", self.request.get_full_path())
        param = self.request.get_full_path()
        param = param.split("/")
        print(param)
        param = param[2]
        print(param)

        # print("the passed get request.: ", kwargs["pk"])
        queryset = queryset.filter(name__icontains = param)
        q2 = Product.objects.filter(index__icontains = param)
        print(q2)
        queryset = queryset.union(q2)
        # pagination
        print(queryset)
        p = Paginator(queryset, 10)
        page = self.request.GET.get("page")
        qs = p.get_page(page)


        return qs

    def get_context_data(self, **kwargs):
        # shop = Shop.objects.get(id = self.kwargs['pk'])
        # form = ProductStockUpdateForm()
        # selected_cat_id = self.kwargs["cat"]
        # if selected_cat_id != 0:
        #     curr_category = Category.objects.get(id = selected_cat_id)
        #     print("asds: ",curr_category)
        # else:
        #     curr_category = "All"
        context = super().get_context_data(**kwargs)
        orders = Order.objects.filter(user = self.request.user)
        orders = orders.filter(completed = False).count()
        # categories = Category.objects.filter(shop = shop)
        cart_items = self.request.user.cart_items()
        # print("cart_items:", cart_items)

        cart_p = self.request.user.cart_prods()
        # print("cart_prods:", cart_p)
        p_ids = [x.id for x in cart_p ]
        # print(p_ids)
        prods = Product.objects.filter(pk__in=p_ids)

        # slides = Slide.objects.filter(user = shop.user)

        cart = Item.objects.filter(cart=self.request.user.cart)
        # for i in cart_items:
        #     print(i)
        #     cart_p.append(i.product)
        context.update({
            # 'shop':shop,
            # "form":form,
            # "categories":categories,
            # "current_category":curr_category,
            "cart_items": cart,
            "prods":prods,
            "orders": orders,
            # "slides":slides,
        })
        return context
          



class ProductCreateView(LoginRequiredMixin, CreateView):
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



class ProductDeleteView(LoginRequiredMixin, DeleteView):
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



class ProductUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'shop/product_update.html'
    form_class = ProductStockUpdateForm

    
    def get_context_data(self, **kwargs):
        curr_prod = Product.objects.get(id = self.kwargs["pk"])
        form = ProductStockUpdateForm(instance = curr_prod)
        prod_id = self.kwargs['pk']
        
        prod = Product.objects.get(id = prod_id)

        queryset = Product.objects.get(id = prod_id)
        context = super().get_context_data(**kwargs)

        context.update({
            'prod':prod,
            'categories':prod.get_categories()
        })
        return context
    
    
    def get_queryset(self): 
        user = self.request.user
        prod_id = self.kwargs["pk"]

        prod = Product.objects.get(id= prod_id)
        queryset = Product.objects.filter(shop = prod.shop)
        return queryset


    def get_success_url(self):
        return reverse('shop:product_update', kwargs = {'pk': self.kwargs['pk']})



class ProductCompareView(LoginRequiredMixin, ListView):    
    template_name = 'shop/product_compare.html'

    def get_queryset(self, **kwargs):

        prod = Product.objects.get(id = self.kwargs["pk"])
        print(prod)
        
        keywords = prod.name.split()
        print(keywords)

        querysetMain = Product.objects.none()
        for i in keywords:
            queryset = Product.objects.filter(name__icontains = i)
            querysetMain = querysetMain.union(querysetMain, queryset)
            print(queryset)

        if prod.index:
            keywords = prod.index.split()
            print(keywords)

            # querysetMain = Product.objects.none()
            for i in keywords:
                queryset = Product.objects.filter(index__icontains = i)
                querysetMain = querysetMain.union(querysetMain, queryset)
                print(queryset)


        return querysetMain

    def get_context_data(self, **kwargs):
        prod_id = self.kwargs["pk"]
        prod = Product.objects.get(id= prod_id)
        context = super().get_context_data(**kwargs)
        cart = Item.objects.filter(cart=self.request.user.cart)

        cart_p = self.request.user.cart_prods()
        # print("cart_prods:", cart_p)
        p_ids = [x.id for x in cart_p ]
        # print(p_ids)
        prods = Product.objects.filter(pk__in=p_ids)


        cart = Item.objects.filter(cart=self.request.user.cart)


        context.update({
            "prod":prod,
            "cart_items":cart,
            "cart_items": cart,
            "prods":prods,
        })
        return context
          


# **************** CATEGORY VIEWS ****************************


class CreateCategoryView(LoginRequiredMixin, ListView):
    template_name = "shop/category_list.html"
    def get_queryset(self):
        shop = Shop.objects.get(id = self.kwargs['pk'])
        return Category.objects.filter(shop = shop)




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


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "shop/category_detail.html"
    
    def get_context_data(self, **kwargs):
        cat = Category.objects.get(id = self.kwargs["pk"])
        context = super().get_context_data(**kwargs)
        
        context.update({"lab": "lasdasd", "cat":cat})
        # print(supp)
        return context

    def get_queryset(self):
        return Category.objects.all()



# **************** SUPPLIER VIEWS *****************************



class CreateSupplierView(LoginRequiredMixin, ListView):
    template_name = "shop/supplier_list.html"
    def get_queryset(self):
        shop = Shop.objects.get(id = self.kwargs['pk'])
        return Supplier.objects.filter(shop = shop)




# normal view for create
def supplier_create(request, pk):
    msg = ''
    form = SupplierModelForm()
    if request.method == 'POST':
        form = SupplierModelForm(request.POST)
        if form.is_valid():
            cat = form.save(commit = False)
            shop = Shop.objects.get(id = pk)
            cat.shop = shop
            cat.save()
            return redirect('shop:suppliers', pk = pk)

        else:
            print('\n\nForm Invalid!!!')
    shop = Shop.objects.get(id = pk)
    suppliers = Supplier.objects.filter(shop = shop)
    context = {'form':form, 'msg':msg, 'suppliers': suppliers}
    return render(request , 'shop/supplier_list.html', context)



def supplier_delete(req, pk):
    lead = Supplier.objects.get(id = pk)
    shop = lead.shop
    lead.delete()
    return redirect("shop:suppliers", pk = shop.id)




class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'shop/supplier_update.html'
    form_class = SupplierUpdateForm

    
    def get_context_data(self, **kwargs):
        curr_supp = Supplier.objects.get(id = self.kwargs["pk"])
        form = SupplierUpdateForm(instance = curr_supp)
        supp_id = self.kwargs['pk']
        
        supp = Supplier.objects.get(id = supp_id)
        # print(prod)
        queryset = Supplier.objects.get(id = supp_id)
        context = super().get_context_data(**kwargs)
        context.update({
            'supplier':supp,
            # 'categories':prod.get_categories()
        })
        print(supp)
        return context
    
    
    def get_queryset(self): 
        user = self.request.user
        supp_id = self.kwargs["pk"]

        supp = Supplier.objects.get(id= supp_id)
        queryset = Supplier.objects.filter(shop = supp.shop)
        return queryset

    
    def get_success_url(self):
        return reverse('shop:supplier-update', kwargs = {'pk': self.kwargs['pk']})



class SupplierDetailView(LoginRequiredMixin, DetailView):
    template_name = "shop/supplier_detail.html"
    
    def get_context_data(self, **kwargs):
        cat = Supplier.objects.get(id = self.kwargs["pk"])
        context = super().get_context_data(**kwargs)
        
        context.update({"lab": "lasdasd", "supp":cat})
        # print(supp)
        return context

    def get_queryset(self):
        return Supplier.objects.all()



# **************** ITEM VIEWS *************************


class ItemCreateView(LoginRequiredMixin, CreateView):
    template_name = 'shop/item_create.html'
    form_class = ItemModelForm
    def get_success_url(self):
        print(self.object.product.shop)
        print("asdsadasd")

        return reverse('shop:home', kwargs = {'pk': self.object.product.shop.id, 'cat':0})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = Product.objects.get(id = self.kwargs["pk"])
        print(product)
        context['prod'] = product
        return context


    def form_valid(self, form):
        prod = form.save(commit=False)
        product_id = self.kwargs['pk']
        prod.product = Product.objects.get(id = product_id)
        prod.cart = self.request.user.cart
        prod.save()
        return super(ItemCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(ItemCreateView, self).get_form_kwargs()
        prod = Product.objects.get(id = self.kwargs["pk"])
        kwargs.update({'prod': prod})
        return kwargs


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
            for i in range(20,50):
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





class ItemUpdateView(LoginRequiredMixin, UpdateView):
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
        
    def get_context_data(self, **kwargs):
        prod_id = self.kwargs['pk']
        
        prod = Item.objects.get(id = prod_id)

        context = super().get_context_data(**kwargs)
        context.update({
            'item':prod,
            "prod":prod.product,
        })
        return context


    def form_valid(self, form):
        prod = form.save(commit=False)
        
        prod.save()
        return super(ItemUpdateView, self).form_valid(form)

    def get_form_kwargs(self):
        # self.kwargs
        # breakpoint()
        it_id = self.kwargs["pk"]
        itm = Item.objects.get(id = it_id)
        prod = itm.product
        kws = super().get_form_kwargs()
        kws.update(prod = prod)
        return kws




class ItemDeleteView(LoginRequiredMixin, DeleteView):
    def get_queryset(self):
        prod_id = self.kwargs['pk']
        print(prod_id)
        prod = Item.objects.get(id = prod_id)
        queryset = Item.objects.filter(product__shop = prod.product.shop)
        return queryset

    template_name = 'shop/item_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = Item.objects.get(id=self.kwargs["pk"])
        context.update({"item":item})
        return context

    def get_success_url(self):
        prod = self.get_object()
        return reverse("shop:home", kwargs = {'pk':prod.product.shop.id, "cat":0})





class CheckoutDetailView(LoginRequiredMixin, ListView):
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
    

# ************* ORDER VIEWS *******************

class OrderCreateView(LoginRequiredMixin, CreateView):
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
        })
        return context



class OrderListCustomerView(LoginRequiredMixin, ListView):
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




class OrderListView(LoginRequiredMixin, ListView):
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




class OrderUpdateView(LoginRequiredMixin, UpdateView):
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
            "order":order,
            "shop":order.shop
        })
        return context
    




class OrderDeleteView(LoginRequiredMixin, DeleteView):
    def get_queryset(self):
        ord_id = self.kwargs['pk']
        print(ord_id)
        order = Order.objects.get(id = ord_id)
        queryset = Order.objects.filter(user = order.user)
        return queryset

    template_name = 'shop/order_delete.html'
    def get_success_url(self):
        prod = self.get_object()
        print("the shop owner is: ")
        try:
            print(self.request.user.shop)
        except:
            print("no attr shop on user")
        if self.request.user.shop:
            return reverse("shop:order-list", kwargs = {'pk':prod.shop.id})
        else:
            return reverse("cart", kwargs = {'pk':prod.user.id})





def OrderDetailViewCustomer(request, pk):
    context ={}
    order_id = pk
    order = Order.objects.get(id = order_id)
    items = OrderItem.objects.filter(order = order)
    context.update({
        "items":items,
        "user":order.user,
        "order":order
    })
    return render(request, "shop/order_detail_customer.html", context=context)


# ***************** PAYMENT VIEWS ******************

def payment_handler(request, pk,  **kwargs):
    print("kwargs in payment_handler: ",kwargs)
    order = Order.objects.get(id = pk)
    print(order)
    # if request.method == "POST":
    # client = razorpay.Client(auth=("rzp_test_0ovBWEVK2aFRht", "omFNDCkZBgjorzpFzNNmfKyd"))
    shop = order.shop
    # print(self.kwargs['pk'])
    pbk = shop.rzp_pb_key[2:-1]
    print(pbk)
    pbk = encrypter.decrypt(pbk.encode())
    pbk = pbk.decode("utf-8")

    prk = shop.rzp_pr_key[2:-1]
    prk = encrypter.decrypt(prk.encode())
    prk = prk.decode("utf-8")
    # shop.save()
    # breakpoint()
    # client = razorpay.Client(auth=(order.shop.rzp_pb_key, order.shop.rzp_pr_key))
    client = razorpay.Client(auth=(pbk, prk))
    # client = razorpay.Client(auth=(prk, pbk))

    amount = order.price * 100
    print(amount)
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
    return render(request, "shop/payment.html", {"order":order, "payment":payment})




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
        # try:
        print(request.POST.get("razorpay_signature") or "Got nothing")
        print(request.POST.get("razorpay_payment_id") or "Got nothing")
        print(request.POST.get("razorpay_order_id") or "Got nothing")
        
        client = razorpay.Client(auth=("rzp_test_0ovBWEVK2aFRht", "omFNDCkZBgjorzpFzNNmfKyd"))
        params_dict = {
            'razorpay_order_id': request.POST.get("razorpay_order_id"),
            'razorpay_payment_id': request.POST.get("razorpay_payment_id"),
            'razorpay_signature': request.POST.get("razorpay_signature")
        }
        order = Order.objects.get(id = request.POST.get("order_id"))
        try: 
            succ = client.utility.verify_payment_signature(params_dict)
        # if succ:
        #     return HttpResponse("Payment Failed.")
            
            order.is_paid = True
            order.signature = request.POST.get("razorpay_signature")
            order.order_id = request.POST.get("razorpay_payment_id")
            order.payment_id = request.POST.get("razorpay_order_id")
            order.save()
        except:
            return render(request, "shop/payment_failed.html")

            
        # except:
        #     print("Failed in success()")
        return redirect("shop:order-detail-customer", pk = order.id)




def map_index(request):

    if request.method == "POST":
        form = request.POST
        if form.is_valid():
            print("SADadsasdasd")
            print(form.data)


    location = gc.osm("Lucknow")
    lat = location.lat
    lon = location.lng
    m = folium.Map(location = [lat, lon], zoom_start = 4)
    folium.Marker([lat, lon], tooltip = "drag to your location").add_to(m)
    # m.save()
    m = m._repr_html_()
    context = {
        "m":m,
    }
    return render(request, "shop/map_index.html", context)





# *********************** SLIDE VIEWS ****************




class SlideListView(LoginRequiredMixin, ListView):
    pass
    template_name = "shop/slide_list.html"
    def get_queryset(self):
        shop = User.objects.get(id = self.kwargs['pk'])
        return Slide.objects.filter(user = shop)



class SlideCreateView(LoginRequiredMixin, CreateView):
    template_name = 'shop/slide_create.html'
    form_class = SlideModelForm
    
    def get_success_url(self):
        # print(self.kwargs['id'])
        # print(self.request.pk)
        # print(self.request.id)
        # print(self.request.shop.id)
        # prod = self.kwargs['id']
        print(self.kwargs)
        return reverse("shop:home", kwargs = {'pk':self.request.user.shop.id, "cat":0})
        # , kwargs = {'pk': prod})
    # to send an email when a new lead is created

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("order:id = ", self.kwargs["pk"])
        user_id = self.kwargs['pk']
        user = User.objects.get(id = user_id)
        slide = Slide.objects.filter(user = self.request.user)
        context.update({
            "slides":slide,
            # "user":order.user,
            # "order":order
        })
        return context
    



    def form_valid(self, form):
        # do whatever u want to do here
        prod = form.save(commit=False)
        shop_id = self.kwargs['pk']
        # print(self)
        # prod.shop = Shop.objects.get(id = shop_id)
        prod.user = self.request.user
        print(self.kwargs['pk'])
        # print(self.get_object())
        
        prod.save()
        return super(SlideCreateView, self).form_valid(form)




def SlideDeleteView(request, pk):
    lead = Slide.objects.get(id = pk)
    # shop = lead.shop
    lead.delete()
    return redirect("shop:slide-create", pk = request.user.id)





