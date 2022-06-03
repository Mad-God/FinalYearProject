from django import forms
from .models import Product, Category, Item, Order, StockFile, Slide, Supplier
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model

User = get_user_model()



class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'name', 'price', 'stock','category', "index", "supplier", "img", 
        )
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(ProductModelForm, self).__init__(*args, **kwargs)
        print("kwargs from the form: ", kwargs, "\nargs from the form: ", args)
        self.fields['category'].widget = forms.CheckboxSelectMultiple()

        print(kwargs)
        print(self.user)
        # exact='mygroup').exists():
        #     del self.fields['confidential']
        # prod = kwargs['instance']
        # shop = prod.shop
        self.fields['category'].queryset = Category.objects.filter(shop = self.user.shop)
        self.fields['supplier'].queryset = Supplier.objects.filter(shop = self.user.shop)
    # def __init__(self, *args, **kwargs):
    #     super(ProductStockUpdateForm, self).__init__(*args, **kwargs)
    #     print("kwargs from the form: ", kwargs, "\nargs from the form: ", args)
    #     self.fields['category'].widget = forms.CheckboxSelectMultiple()
    #     # we have to use try because this form is being initated at other pages too, and then, the instace keyword is not found in the kwargs
    #     try:
    #         prod = kwargs['instance']
    #         shop = prod.shop
    #         self.fields['category'].queryset = Category.objects.filter(shop = shop)
    #         self.fields['supplier'].queryset = Supplier.objects.filter(shop = shop)
    #     except:
    #         pass
      

class ProductStockUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            'stock', 'price', 'category', "index", "supplier", "img",
        )
    
    def __init__(self, *args, **kwargs):
        super(ProductStockUpdateForm, self).__init__(*args, **kwargs)
        print("kwargs from the form: ", kwargs, "\nargs from the form: ", args)
        self.fields['category'].widget = forms.CheckboxSelectMultiple()
        # we have to use try because this form is being initated at other pages too, and then, the instace keyword is not found in the kwargs
        try:
            prod = kwargs['instance']
            shop = prod.shop
            self.fields['category'].queryset = Category.objects.filter(shop = shop)
            self.fields['supplier'].queryset = Supplier.objects.filter(shop = shop)
        except:
            pass

      


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            'name',
        )






class SupplierModelForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = (
            'name',"address", "phone", "email", 
        )




class SupplierUpdateForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = (
            'name',"address", "phone", "email", 
        )





class SlideModelForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = (
            'text',
            'img',
        )




class ItemModelForm(forms.ModelForm):
    # quantity = forms.IntegerField(max_value = 8)
    class Meta:
        model = Item
        fields = (
            'quantity',
        )


        print(dir(forms.IntegerField))
    
    def __init__(self, *args, **kwargs):
        prod = kwargs.pop('prod')
        super(ItemModelForm, self).__init__(*args, **kwargs)
        print("kwargs from the form: ", kwargs, "\nargs from the form: ", args)
        self.fields["quantity"] = forms.IntegerField(max_value = prod.stock, min_value = 1)
        self.fields['quantity'].widget = forms.NumberInput()

        print(kwargs)





class StockUpdateForm(forms.ModelForm):
    # product_column_name = forms.CharField(max_length=30)
    # stock_column_name = forms.CharField(max_length=30)
    # price_column_name = forms.CharField(max_length=30)
    # stock_file = forms.FileField(required=True)
    class Meta:
        model = StockFile
        fields = (
             'name_column_name', 'price_column_name', 'stock_column_name', 'stock_file'
        )




class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'address', 'delivery', 'cash_on_pickup', 'instruction'
        )

        def __init__(self, *args, **kwargs):
            self.fields["address"].widget.attrs["class"] = "address-input"



class OrderModelForm2(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'address', 'delivery', 'instruction'
        )



class OrderUpdateModelForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'completed',
        )