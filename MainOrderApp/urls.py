from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('product', views.product_list, name='product'),
    path('inventory', views.inventory, name='inventory'),
    path('change_password/', views.change_password, name='change_password'),
    path('add_purchase_item/', views.add_purchase_item, name='add_purchase_item'),
]
