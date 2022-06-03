from django import forms
from .models import User, Shop
from shop.models import Order
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', "email", "phone", 'pfp', 'address')
        # field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['phone'].widget = forms.TextInput(attrs={
            'id': 'phone_field',
            "min":"1000000000",
            "max":"9999999999",
            "type":"number",
            })
        self.fields['email'].widget = forms.TextInput(attrs={"type":"email"})



class ConfirmUserForm(forms.Form):
    # class Meta:
    #     model = User
    #     fields = ('username', "Password")
        
    #     # field_classes = {'username': UsernameField}
    
    # def __init__(self, *args, **kwargs):
    #     super(ConfirmUserForm, self).__init__(*args, **kwargs)
        
    #     self.fields['password'].widget = forms.PasswordInput()
    username = forms.CharField(initial = "")
    password = forms.CharField(widget=forms.PasswordInput(), initial = "")

class UpdateBankDetailsForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('rzp_pr_key', "rzp_pb_key")
        
        # field_classes = {'username': UsernameField}
    
    def __init__(self, *args, **kwargs):
        super(UpdateBankDetailsForm, self).__init__(*args, **kwargs)
        
        self.fields['rzp_pr_key'].label = "Razorpay Private Key"
        self.fields['rzp_pb_key'].label = "Razorpay Public Key"




class ShopCreateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name', "category", "pfp", "open_time", "close_time", "phone", "email", "address","rzp_pr_key", "rzp_pb_key")
        
    def __init__(self, *args, **kwargs):
        super(ShopCreateForm, self).__init__(*args, **kwargs)
        self.fields['close_time'].widget = forms.DateInput(attrs={'class':'timepicker'})
        self.fields['rzp_pr_key'].label = "Enter Razorpay Public Key"
        self.fields['rzp_pb_key'].label = "Enter Razorpay Private Key"
        self.fields['rzp_pr_key'].widget = forms.PasswordInput( )
        self.fields['rzp_pb_key'].widget = forms.PasswordInput()
        self.fields['rzp_pb_key'].initial = ""
        self.fields['rzp_pr_key'].initial = ""

        self.fields['phone'].widget = forms.TextInput(attrs={
            'id': 'phone_field',
            "min":"1000000000",
            "max":"9999999999",
            "type":"number",
            })
        self.fields['email'].widget = forms.TextInput(attrs={"type":"email"})





class ShopUpdateForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name', "pfp", "open_time", "close_time", "phone", "email", "address")
        # widgets = {
        #     'phone':PhoneNumberField()
            # "open_time":forms.TimeField(),
            # "close_time":forms.TimeField(),
        # }
    def __init__(self, *args, **kwargs):
        super(ShopUpdateForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget = forms.TextInput(attrs={
            'id': 'phone_field',
            "min":"1000000000",
            "max":"9999999999",
            "type":"number",
            })
        self.fields['email'].widget = forms.TextInput(attrs={"type":"email"})



class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', "email", "phone", 'pfp', 'address')
        # field_classes = {'username': UsernameField}
        



class OrderCreateForm(forms.Form):
    class Meta:
        model = Order
        fields = ('address', 'description', )