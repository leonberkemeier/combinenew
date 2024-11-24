from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.


class ProjectCategory(models.Model):
    created_at=models.DateField(default=date.today)
    name = models.TextField(max_length=100)
    user= models.IntegerField(default=User.id)

    def __str__(self):
        return str(self.id) + ' '+ self.name
    
class Project(models.Model):
    created_at=models.DateField(default=date.today)
    name = models.TextField(max_length=100)
    user= models.IntegerField(default=User.id)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' '+ self.name
    
class Card(models.Model):
    created_at=models.DateField(default=date.today)
    user= models.IntegerField(default=User.id)
    title=models.TextField(max_length=100)
    front=models.TextField(max_length=100)
    back=models.TextField(max_length=100)
    project=models.ForeignKey(Project, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.id) + ' '+ self.name
    