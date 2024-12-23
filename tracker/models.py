from django.db import models
from datetime import date

# Create your models here.

# TRACKER

class ExpensesItem(models.Model):
    
    
    amount = models.FloatField(null=True)
    purpose = models.CharField(max_length=100, null=True) 
    date = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return (str(self.amount) +" "+self.purpose +" "+ str(self.date))
    

class Purpose(models.Model):
    purpose = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.purpose
    
class Networth(models.Model):
    incomeM = models.FloatField(null=True)
    balance = models.FloatField(null=True)
    assets = models.FloatField(null=True)

    def __str__(self):
        return (str(self.incomeM) + " "+ str(self.balance) +" "+ str(self.assets))
    

class FixedCost(models.Model):
    amount = models.FloatField(null=True)
    purpose = models.CharField(max_length=100, null=True)

    def __str__(self):
        return (str(self.amount) + " "+ str(self.purpose))
    
class Income(models.Model):
    income = models.IntegerField(default=0, null=False)
    date = models.DateField(null=True, blank=True)
    comment = models.CharField(max_length=100, null=True, blank=True)
    tax =models.BooleanField(default=False)
    def __str__(self) -> str:
        return (str(self.income) + ' ' + str(self.date))   


