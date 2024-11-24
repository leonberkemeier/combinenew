from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   path('cards',views.index, name="cards"),
   path('login',views.loginPage, name="login"),
   path('addPC',views.addProjectCategory, name='addPC'),
   path('addProject', views.addProject, name='addProject')
]