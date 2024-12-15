from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   path('addexpense', views.addexpense, name='addexpense'),
    path('addpurpose', views.addpurpose, name='addpurpose'),
    path('addnet', views.addnetworth, name='addnetworth'),
    path('addFixedCost', views.addFixedCost, name='addFixedCost'),
    path('addincome', views.addincome, name='addincome'),

    path('edit_expense/<str:pk>/', views.editexpense, name='edit_expense'),
    path('edit_purpose/<str:pk>/', views.editpurpose, name='edit_purpose'),
    path('edit_net/<str:pk>/', views.editnetworth, name='editnetworth'),
    path('editfixedcost/<str:pk>/', views.editFixedCost, name='editfixedcost'),
    path('editincome/<str:pk>/', views.editincome, name='editincome'),

    path('delete_expense/<str:pk>/', views.deleteexpense, name='delete_expense'),
    path('delete_purpose/<str:pk>/', views.deletepurpose, name='delete_purpose'),
    path('deletefixedcost/<str:pk>/', views.deleteFixedCost, name='deletefixedcost'),
     path('deleteincome/<str:pk>/', views.deleteincome, name='deleteincome'),

     path('tracker', views.tracker, name='tracker'),
    path('list', views.list, name='list'),
    path('balance',views.balance, name='balance'),
    path('assets',views.assets, name='assets'),
]