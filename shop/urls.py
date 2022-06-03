from django.contrib import admin
from django.urls import path
from shop import views

app_name = 'shop' 

urlpatterns = [
    # products
    path('<int:pk>/<int:cat>', views.ProductListView.as_view(), name = 'home'),
    path('<int:pk>/create', views.ProductCreateView.as_view(), name = "product_create"),
    path('delete/<int:pk>', views.ProductDeleteView.as_view(), name = "product_delete"),
    path('update/<int:pk>', views.ProductUpdateView.as_view(), name = "product_update"),
    path('compare/<int:pk>', views.ProductCompareView.as_view(), name = "product_compare"),
    path('<pk>/all', views.ProductListWholeView.as_view(), name = "product_all"),
    
    
    # others
    path('item-create/<int:pk>', views.ItemCreateView.as_view(), name = 'item-create'),
    path('item-update/<int:pk>', views.ItemUpdateView.as_view(), name = 'item-update'),
    path('item-delete/<int:pk>', views.ItemDeleteView.as_view(), name = 'item-delete'),
    path('order-create/<int:pk>', views.OrderCreateView.as_view(), name = 'order-create'),
    path('order-list/<int:pk>', views.OrderListView.as_view(), name = 'order-list'),
    path('order-list-customer/<int:pk>', views.OrderListCustomerView.as_view(), name = 'order-list-customer'),
    path('order-update/<int:pk>', views.OrderUpdateView.as_view(), name = 'order-update'),
    path('order-delete/<int:pk>', views.OrderDeleteView.as_view(), name = 'order-delete'),
    path('order-detail-customer/<int:pk>', views.OrderDetailViewCustomer, name = 'order-detail-customer'),
    path('stock-update/<int:pk>', views.StockUpdateView, name = 'stock-update'),
    path('map-index', views.map_index, name = 'map-index'),


    # categories
    path('<int:pk>/categories', views.category_create, name = 'categories'),
    path('category-delete/<int:pk>', views.category_delete, name = 'category-delete'),
    path('category-detail/<int:pk>', views.CategoryDetailView.as_view(), name = 'category-detail'),


    # suppliers
    path('<int:pk>/suppliers', views.supplier_create, name = 'suppliers'),
    path('supplier-update/<int:pk>', views.SupplierUpdateView.as_view(), name = 'supplier-update'),
    path('supplier-delete/<int:pk>', views.supplier_delete, name = 'supplier-delete'),
    path('supplier-detail/<int:pk>', views.SupplierDetailView.as_view(), name = 'supplier-detail'),

    # slides
    path('slide-create/<int:pk>', views.SlideCreateView.as_view(), name = 'slide-create'),
    path('slide-list/<int:pk>', views.SlideListView.as_view(), name = 'slide-list'),
    path('slide-delete/<int:pk>', views.SlideDeleteView, name = 'slide-delete'),

    # shop
    path('shop-update/<int:pk>', views.ShopUpdateView.as_view(), name = 'shop-update'),
    path('shop-confirm-user', views.confirm_user_view, name = 'confirm-user'),
    path('update-bank-detail/<int:pk>', views.BankDetailUpdateView.as_view(), name = 'update-bank'),

]
