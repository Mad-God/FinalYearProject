from django.contrib import admin
from django.urls import path
from base import views

app_name = 'base'

urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),
    # path('leads_list', views.LeadListView.as_view(), name = 'leads_list'),
    # path('create', views.LeadCreateView.as_view(), name = "lead_create"),
    # path('detail/<int:pk>', views.LeadDetailView.as_view(), name = 'lead_detail'),
    # path('lead_update/<int:pk>', views.LeadUpdateView.as_view(), name = 'lead_update'),
    # path('lead_delete/<int:pk>', views.LeadDeleteView.as_view(), name = 'lead_delete'),
    # path('assign_agent/<int:pk>', views.AssignAgentView.as_view(), name = "assign_agent"),
    # path('category_update/<int:pk>', views.LeadCategoryUpdateView.as_view(), name = "category_update"),
    # path('category_list', views.CategoryListView.as_view(), name = 'category_list'),
    
    # path('category_detail/<int:pk>', views.CategoryDetailView.as_view(), name = 'category_detail'),

]
