from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.


class ProjectCategory(models.Model):
    created_at=models.DateField(default=date.today)
    name = models.TextField(max_length=100)
    user= models.TextField(max_length=100)

    def __str__(self):
        return str(self.id) + ' '+ self.name
    
class Project(models.Model):
    created_at=models.DateField(default=date.today)
    name = models.TextField(max_length=100)
    user= models.TextField(max_length=100)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' '+ self.name
    
class Card(models.Model):
    created_at=models.DateField(default=date.today)
    user= models.TextField(max_length=100)
    title=models.TextField(max_length=100)
    front = models.ImageField(upload_to='Cards/front/', null=True)
    back = models.ImageField(upload_to='Cards/back/', null=True)
    fronttext = models.CharField(max_length=100, null=True)
    backtext = models.CharField(max_length=100, null=True)
    project=models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id) + ' '+ self.title
    

