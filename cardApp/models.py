from django.db import models
from datetime import date
from django.contrib.auth.models import User
# Create your models here.


class ProjectCategory(models.Model):
    created_at=models.DateField(default=date.today)
    name = models.TextField(max_length=100)
    user= models.TextField(default=User)

    def __str__(self):
        return str(self.id) + ' '+ self.name
    
class Project(models.Model):
    created_at=models.DateField(default=date.today)
    name = models.TextField(max_length=100)
    user= models.TextField(default=User)
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ' '+ self.name