from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
   path('cards',views.index, name="cards"),
   path('login',views.loginPage, name="login"),
   path('logout', views.logoutUser, name='logout'),
   path('addPC',views.addProjectCategory, name='addPC'),
   path('addProject', views.addProject, name='addProject'),
   path('addCard', views.addCard, name="addCard"),
   path('addCard/<int:id>', views.addCard, name="addCard"),
   path('projects', views.projects,name="projects"),
   path('projects/<int:id>',views.show_project, name="myproject_details"),
   path('projects/<int:id>/add',views.addCard, name="addCard")
]