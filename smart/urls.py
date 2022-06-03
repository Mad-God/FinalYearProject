from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (
        LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, 
        PasswordResetConfirmView, PasswordResetCompleteView, 
    )
from base.views import SignupView, ProfileDetailView, CartView ,CheckoutDetailView, ProfileUpdateView
from shop.views import payment_handler_with_order_id, success, CheckoutDetailView, payment_handler, ShopCreateView
# from leads.views import index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls', namespace = 'base')),
    path('shop/', include('shop.urls', namespace = 'shop')),
    path('login/', LoginView.as_view(),name = 'login'),
    path('logout/', LogoutView.as_view(),name = 'logout'),
    path('profile/<int:pk>', ProfileDetailView.as_view(),name = 'profile'),
    path('profile-update/<int:pk>', ProfileUpdateView.as_view(),name = 'profile-update'),
    path('cart/<int:pk>', CartView,name = 'cart'),
    # path('checkout/<int:pk>', CheckoutDetailView,name = 'checkout'),
    path('checkout/<int:pk>', CheckoutDetailView.as_view(),name = 'checkout'),
    path('signup/', SignupView.as_view(),name = 'signup'),
    # path('password_reset/', PasswordResetView.as_view(),name = 'password_reset'),
    # path('payment/<int:pk>', payment_handler_with_order_id, name = 'payment'),
    path('payment/<int:pk>', payment_handler, name = 'payment'),
    path('success', success, name = 'success-payment'),
    path('password_reset/', PasswordResetView.as_view(),name = 'password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(),name = 'password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),name = 'password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(),name = 'password_reset_complete'),

    # shop views
    path("shop_create", ShopCreateView.as_view(), name="shop-create")
    
]