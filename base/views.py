from django.shortcuts import render, HttpResponseRedirect
from django.http import HttpResponse
from .models import Shop, User
from shop.models import Item, Cart, Slide
# from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.shortcuts import redirect, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
# from agents.mixins import OrganiserLoginRequiredMixin

# Create your views here.


class HomeView(LoginRequiredMixin, ListView):
    template_name = 'base/shop_list.html'

    def get_context_data(self, **kwargs):
        superusers = User.objects.get(is_superuser=True)
        context = super().get_context_data(**kwargs)
        slides = Slide.objects.filter(user = superusers)
        sl1 = Slide.objects.first()
        context.update({
            'slides':slides,
            'sl':sl1,
            "hello":"asdasdsadsad"
            # 'categories':prod.get_categories()
        })
        return context
    
    def form_valid(self, **kwargs):
        print(self)
        print(kwargs)
        print("\n\n\n\n\nasdkjasdbjhabsdjhbasd\n\n\n\n")
        if self.request.GET.get("q"):
            print("\n\n\n\n",self.request.POST.get("q"))

    def get(self, *args, **kwargs):
        pass


    def get_queryset(self, **kwargs):
        queryset = Shop.objects.all()
        return queryset
    


    def get(self, *args, **kwargs):
        try:
            if self.request.user.shop:
                return redirect('shop:home', pk=self.request.user.shop.id, cat=0)
        except:
            if self.request.GET:
                print(self.request.GET.get("q"))
                return redirect("shop:product_all", pk = self.request.GET.get("q"))
            return super(HomeView, self).get(*args, **kwargs)
            # return super(HomeView, self).get(*args, **kwargs)



class SignupView(CreateView):
    template_name = "registration/user_create.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")



class ProfileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'registration/user_detail.html'
    context_object_name = 'user'


    def get_queryset(self):
        return User.objects.all()




class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/user_detail.html'
    context_object_name = 'user'


    def get_queryset(self):
        return User.objects.all()



class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'registration/user_update.html'
    form_class = CustomUserUpdateForm

    
    def get_context_data(self, **kwargs):
        curr_supp = User.objects.get(id = self.kwargs["pk"])
        form = CustomUserUpdateForm(instance = curr_supp)
        # supp_id = self.kwargs['pk']
        
        # supp = Supplier.objects.get(id = supp_id)
        # print(prod)
        # queryset = Supplier.objects.get(id = supp_id)
        context = super().get_context_data(**kwargs)
        context.update({
            'supplier':curr_supp,
            # 'categories':prod.get_categories()
        })
        print(curr_supp)
        return context
    
    
    def get_queryset(self): 
        user = self.request.user
        # supp_id = self.kwargs["pk"]

        # supp = Supplier.objects.get(id= supp_id)
        queryset = User.objects.filter(id = user.id)
        return queryset

    
    def get_success_url(self):
        return reverse('profile', kwargs = {'pk': self.kwargs['pk']})



def CartView(request, pk):
    msg = ''
    user = request.user
    print(user)
    shops = Shop.objects.all()
    items = request.user.cart.items.all()
    total = {}
    shops = set()
    for i in items:
        shops.add(i.product.shop)
        # if str(i.product.shop.id) in  total:
        if i.product.shop.id in  total:
            # total[str(i.product.shop.id)] += i.product.price * i.quantity
            total[i.product.shop.id] += i.product.price * i.quantity

        else:
            # total[str(i.product.shop.id)] = i.product.price * i.quantity
            total[i.product.shop.id] = i.product.price * i.quantity

    print(total)
    context = {'msg':msg, 'items': items, 'shops': shops, 'total':total}
    return render(request , 'base/cart.html', context)





def CheckoutDetailView(req, pk):

    return HttpResponse("asdadas")