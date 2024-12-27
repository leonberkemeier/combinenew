from django.shortcuts import render, redirect

from .forms import ExpensesForm, PurposeForm, NetworthForm, FixedCostForm, IncomeForm
from django.contrib import messages
from datetime import date,datetime
import datetime as dt

from .models import ExpensesItem, Purpose, Networth ,FixedCost, Income
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import calendar
from calendar import monthrange
from django.core import serializers
from django.http import JsonResponse
import sys
from django.db.models import Sum

import json
# Create your views here.



@login_required(login_url='login')
def tracker(request):
    expenses, income2, month, year = datefilter(request)
    
    if year is not None and month is not None:
        days = calendar.monthrange(int(year),int(month))[1]

    current_time = dt.datetime.now()
    current_day = current_time.day

    networth = Networth.objects.first()
    income = networth.incomeM

    incomesum=income2.aggregate(Sum('income')).get('income__sum')
    # income = incomesum
    
    if incomesum == None:
        incomesum = 0
    
    assets = networth.assets
    rel_balance = networth.balance
    avgincome = round(incomesum/days, 2)
    
    # Array of days
    days_array=[]    

    for i in range(days):
        days_array.append(i+1)
    
    # Array of Expenses
    expenses_array = []

    sumExpens=0
    sumExpenses=round(sumExpens,2)
    

    for i in range(days):
        
        seqs = expenses.filter(date__day = i).aggregate(Sum('amount')).get('amount__sum')

        if seqs == None:
            seqs = 0

        expenses_array.append(float(seqs))
        sumExpenses+=int(seqs)
    
    totalexpenses = sumExpenses 

    average_networth_array = []
    for i in range(days):
        if i <= current_day:
            rel_balance =round(rel_balance + avgincome - expenses_array[i],2)
            average_networth_array.append(rel_balance)
        else:
            rel_balance=rel_balance
            average_networth_array.append(rel_balance)
    

    expenses_and_income_pd=[]
    for i in range(days):
        if i <= current_day:
            difday = avgincome - expenses_array[i]
            expenses_and_income_pd.append(difday)
        else:
            difday =0
            expenses_and_income_pd.append(difday)
        
    pl = purposeList(filter='purpose') 
    # print(pl)
    el = expenseList(expenses)

    sumcosts = sumExpenses

    #Sum fixed Costs
    
    sumfixedcosts=0
    fixedCosts = FixedCost.objects.all()
    for i in range(len(fixedCosts)):
        sumfixedcosts += fixedCosts[i].amount
    # print(sumfixedcosts)

    totalexpenses=sumfixedcosts+sumcosts

    balance = incomesum - totalexpenses


    addincomeform = IncomeForm(request.POST)
    addexpenseform = ExpensesForm(request.POST)

    # print(el)
    context={
        'income':incomesum,
        'totalexpenses':totalexpenses,
        'assets':assets,
        'balance':balance,

        'networth':networth,

        'days_array':days_array,
        'expenses_array': expenses_array,
        'rel_balance':rel_balance,
        'average_networth_array': average_networth_array,
        'expenses_and_income_pd':expenses_and_income_pd,
        
        'days':days,
        'year':year,
        'month':month,

        'addincomeform':addincomeform,
        'addexpenseform':addexpenseform,

        'pl': pl,
        'el': el,
    }

    return render(request, "tracker/tracker.html", context)

@login_required(login_url='login')
def list(request):
    
    # current_year = datetime.now().year
    # current_month = datetime.now().month
    
    # year = request.GET.get('year', current_year)
    # month = request.GET.get('month', current_month)

    # if year is not None and year != '':
    #     expenses = expenses.filter(date__year=year)
    
    # if month is not None and month != '':
    #     expenses = expenses.filter(date__month =month)

    # pqs =Purpose.objects.values_list('purpose' ,flat= True)
    # print(pqs[0])
    # n = Networth.objects.all()
    # nf = netfilter(n)

    # pqs = purposeList(filter='purpose')
    # print(pqs)
    # eql = expenseList(expenses)
    # print(eql)
  
    expenses, income2, month, year = datefilter(request)

    incomesum=income2.aggregate(Sum('income')).get('income__sum')
    
    if incomesum == None:
        incomesum = 0

    purposes = Purpose.objects

    
    
    if year is not None and month is not None:
        days = calendar.monthrange(int(year),int(month))[1]

    try:
        networth = Networth.objects.first()
        income = incomesum
        balance = networth.balance
        assets = networth.assets
        rel_balance = networth.balance
        avgincome = round(income/days, 2)
    except:
        return

    #Sum fixed Costs
    sumfixedcosts=0
    fixedCosts = FixedCost.objects.all()
    for i in range(len(fixedCosts)):
        sumfixedcosts += fixedCosts[i].amount
    # print(sumfixedcosts)
    # Array of days
    days_array=[]    

    for i in range(days):
        days_array.append(i+1)

    # print(days_array)
    networth_array=[]

    for i in range(days):
        days_array.append(i+1)
        rel_balance = round(rel_balance+avgincome,2)
        networth_array.append(rel_balance)

    # Array of Expenses
    expenses_array = []

    sumExpens=0
    sumExpenses=round(sumExpens,2)

    for i in range(days):
        
        seqs = expenses.filter(date__day = i).aggregate(Sum('amount')).get('amount__sum')

        if seqs == None:
            seqs = 0

        expenses_array.append(float(seqs))
        sumExpenses+=int(seqs)
    
    sumcosts = sumExpenses

    totalexpenses=sumfixedcosts+sumcosts

    # print(expenses_array)
    # print(len(expenses_array))
    pl = purposeList(filter='purpose') 
    # print(pl)
    el = expenseList(expenses)
    # print(el)

    balance = incomesum - totalexpenses

    addincomeform = IncomeForm(request.POST)
    addexpenseform = ExpensesForm(request.POST)
    addFCForm = FixedCostForm(request.POST)

    context = {
        'income':income,
        'totalexpenses':totalexpenses,
        'sumcosts':sumcosts,
        'assets':assets,
        'balance':balance,

        'expenses' : expenses,
        'purposes':purposes,
        'month':month,
        'year':year,
        
        'days_array':days_array,
        'expenses_array': expenses_array,

        'days':days,
        'avgincome': avgincome,
        # 'expenses_and_income_pd':expenses_and_income_pd,
        'fixedCosts': fixedCosts,
        'sumfixedcosts':sumfixedcosts,

        'addincomefrom':addincomeform,
        'addexpenseform':addexpenseform,
        'addFCForm': addFCForm,

        'pl':pl,
        'el':el
    }
    return render(request, 'tracker/list.html', context)

@login_required(login_url='login')
def balance(request):
    

    expenses,income2, month, year = datefilter(request)
    # print(expenses)

    # print(year, month)
    if year is not None and month is not None:
        days = calendar.monthrange(int(year),int(month))[1]

    taxincome=income2.filter(tax=1)
    

    ntaxincome=income2.filter(tax=0)
    
    # print(year, month)
    incomesum=income2.aggregate(Sum('income')).get('income__sum')
    if taxincome == None:
        taxincomesum = 0
    else:
        taxincomesum=taxincome.aggregate(Sum('income')).get('income__sum')
    
    if ntaxincome == None:
        ntaxincomesum = 0
    else:
        ntaxincomesum=ntaxincome.aggregate(Sum('income')).get('income__sum')
    
    #Steuerliche Abgaben STEUERSAETZE
    
    if taxincomesum == None:
        taxincomesum =0

    if taxincomesum <1300:  
        LS = 0
    else:
        LS = 15
    # LS =0
    KS=4
    RV=9.3
    KV=8.3
    AV=1.3
    PV=2.3

    #Resultierende Abgaben
    LSA = round(taxincomesum * LS /100,2)
    KSA = round(taxincomesum * KS / 100,2)
    RVA = round(taxincomesum * RV/ 100,2)
    KVA = round(taxincomesum * KV/100,2)
    AVA = round(taxincomesum * AV/100,2)
    PVA = round(taxincomesum * PV/100,2)
    SummeAbgaben = round(LSA + KSA + RVA + KVA + AVA + PVA,2)

    posttax = taxincomesum - SummeAbgaben
    
    if incomesum == None:
        incomesum = 0


    totalincome = posttax + ntaxincomesum

    # Array of Expenses
    expenses_array = []

    sumExpens=0
    sumExpenses=round(sumExpens,2)

    for i in range(days):
        
        seqs = expenses.filter(date__day = i).aggregate(Sum('amount')).get('amount__sum')

        if seqs == None:
            seqs = 0

        expenses_array.append(float(seqs))
        sumExpenses+=int(seqs)
    

    #Expenses
       
    purposelist = Purpose.objects.all()
    for purposeitem in purposelist:
        # purposeitem.expense = expenses.filter(purpose=purposeitem).aggregate(Sum('amount')).get('amount__sum')
        summeexpenses = expenses.filter(purpose=purposeitem).aggregate(Sum('amount')).get('amount__sum')
        # None = 0:
        if summeexpenses == None:
            summeexpenses = 0
            purposeitem.expense = summeexpenses
        else:
            purposeitem.expense = summeexpenses
        
        if sumExpenses == 0:
            purposeitem.percent = 0
        else:
            purposeitem.percent = round(summeexpenses / sumExpenses , 2)
    
    # for i in purposelist:
    #     print('purpose')
    #     print(i.purpose)
        
    #     print('amount')
    #     print(i.expense)
    #     print('//')

    #Sum fixed Costs
    sumfixedcosts=0
    fixedCosts = FixedCost.objects.all()
    for i in range(len(fixedCosts)):
        sumfixedcosts += fixedCosts[i].amount
    fsumfixedcosts =f"{sumfixedcosts:.2f}"

    sumfixedcostsrate =f"{sumfixedcosts/incomesum:.2f}"

    sumcosts = sumExpenses
    sumcostsrate = f"{sumcosts/incomesum:.2f}"


    totalexpenses=sumfixedcosts+sumcosts
    ftotalexpenses = f"{totalexpenses:.1f}"

    sparplanrate = 10.00
    sparplan = incomesum/sparplanrate
    fsparplan =f"{sparplan:.2f}"

    profitloss = totalincome - totalexpenses - sumfixedcosts    
    balance = totalincome - sumcosts -sumfixedcosts
    balance2 = balance - sparplan
    print(balance2)
    
    context={
        
        'totalexpenses':ftotalexpenses,
        'balance': balance,
        'income':incomesum,

        'days':days,
        'year':year,
        'month':month,

        'ntaxincomesum':ntaxincomesum,
        'taxincomesum':taxincomesum,

        'LS':LS,
        'KS':KS,
        'RV':RV,
        'KV':KV,
        'AV':AV,
        'PV':PV,

        'LSA':LSA,
        'KSA':KSA,
        'RVA':RVA,
        'KVA':KVA,
        'AVA':AVA,
        'PVA':PVA,
        'SummeAbgaben':SummeAbgaben,
        'posttax':posttax,
        'totalincome':totalincome,

        'purposelist': purposelist,
        'fixedCosts':fixedCosts,
        'sumcosts':sumcosts,
        'sumcostsrate':sumcostsrate,
        'sumfixedcosts':sumfixedcosts,
        'sumfixedcostsrate':sumfixedcostsrate,

        'sparplan':fsparplan,
        'sparplanrate':sparplanrate,
        'balance2':balance2


    }
    return render(request, 'tracker/balance.html', context)

def assets(request):
    networth = Networth.objects.first()
    income = networth.incomeM
    balance = networth.balance
    assets = networth.assets

    expenses, month, year = datefilter(request)

    if year is not None and month is not None:
        days = calendar.monthrange(int(year),int(month))[1]


    # Array of Expenses
    expenses_array = []

    sumExpens=0
    sumExpenses=round(sumExpens,2)

    for i in range(days):
        
        seqs = expenses.filter(date__day = i).aggregate(Sum('amount')).get('amount__sum')

        if seqs == None:
            seqs = 0

        expenses_array.append(float(seqs))
        sumExpenses+=int(seqs)
    
    totalexpenses = sumExpenses 

    context={
        'income':income,
        'totalexpenses':totalexpenses,
        'assets':assets,
        'balance':balance,

    }
    return render(request, 'tracker/assets.html', context)

def sumfixedcosts():
    sumfixedcosts=0
    fixedCosts = FixedCost.objects.all()
    for i in range(len(fixedCosts)):
        sumfixedcosts += fixedCosts[i].amount
    print(sumfixedcosts)
    
    return sumfixedcosts

def datefilter(request):
    current_year = datetime.now().year
    current_month = datetime.now().month
    year = request.GET.get('year', current_year)
    month = request.GET.get('month', current_month)
    expenses =ExpensesItem.objects
    income =Income.objects

    if year is not None and year != '':
        expenses = expenses.filter(date__year=year)
        income = income.filter(date__year=year)
    
    if month is not None and month != '':
        expenses = expenses.filter(date__month =month)
        income = income.filter(date__month=month)
    expenses = expenses.all()
    income = income.all()
    
    return (expenses,income, month, year)

def netfilter(n):
    # print(n)
    nf = n.filter(balance=222)
    # print(nf)
    return nf

def purposeList(filter):
    lp=[]
    pqs =Purpose.objects.values_list(filter ,flat= True)
    for i in range(len(pqs)):
        lp.append(pqs[i])
    lpqs = lp
    return lpqs

def expenseList(exp):
    el = []
    pl = purposeList(filter='purpose')
    # print(pl)

    for i in range(len(pl)):
        
        seqs =exp.filter(purpose = pl[i]).aggregate(Sum('amount')).get('amount__sum')

        # New Purpose might have no Expenses under their name: so the Value is Null
        # Reasigning the Value to zero does not fukc with the JS
        
        if seqs == None:
            seqs = 0
        # print(seqs)
        el.append(seqs)
        
    # print(el)
    return el



# Expense
@login_required(login_url='login')
def addexpense(request):
    
    form = ExpensesForm(request.POST)

    if request.method == 'POST':
        #print('printpost',request.POST)
        form = ExpensesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/list')
 
    context = {'form' : form }
    
    return render(request, "tracker/expenseadd.html" ,context)



@login_required(login_url='login')
def editexpense(request, pk):

    expense = ExpensesItem.objects.get(id=pk)
    form = ExpensesForm(instance=expense)

    if request.method == 'POST':

        #print('hey', request.POST)
        form = ExpensesForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('/list')
 
    context={
        'form':form,
        'expense':expense,

    }
    return render(request, "tracker/expensesedit.html" ,context)

@login_required(login_url='login')
def deleteexpense(request, pk):

    expense = ExpensesItem.objects.get(id=pk)
    form = ExpensesForm(instance=expense)

    if request.method == 'POST':

        expense.delete()
        return redirect('/list')
 
    context={
        'form':form,
        'expense':expense
    }
    return render(request, "tracker/expensedelete.html" ,context)


# INCOME

@login_required(login_url='login')
def addincome(request):
    
    form = IncomeForm(request.POST)

    if request.method == 'POST':
        #print('printpost',request.POST)
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/list')
 
    context = {'form' : form }
    
    return render(request, "tracker/expenseadd.html" ,context)

@login_required(login_url='login')
def editincome(request, pk):

    expense = Income.objects.get(id=pk)
    form = IncomeForm(instance=expense)

    if request.method == 'POST':

        #print('hey', request.POST)
        form = IncomeForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('/list')
 
    context={
        'form':form,
        'expense':expense,

    }
    return render(request, "tracker/expensesedit.html" ,context)

@login_required(login_url='login')
def deleteincome(request, pk):

    expense = Income.objects.get(id=pk)
    form = IncomeForm(instance=expense)

    if request.method == 'POST':

        expense.delete()
        return redirect('/list')
 
    context={
        'form':form,
        'expense':expense
    }
    return render(request, "tracker/expensedelete.html" ,context)





# Purpose

@login_required(login_url='login')
def addpurpose(request):
    
    form = PurposeForm(request.POST)

    if request.method == 'POST':
        #print('printpost',request.POST)
        form = PurposeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/list')
 
    context = {'form' : form }
    
    return render(request, "tracker/purposeadd.html" ,context)

@login_required(login_url='login')
def editpurpose(request, pk):

    purpose = Purpose.objects.get(id=pk)
    form = PurposeForm(instance=purpose)

    if request.method == 'POST':

        #print('hey', request.POST)
        form = PurposeForm(request.POST, instance=purpose)
        if form.is_valid():
            form.save()
            return redirect('/tracker/list')
 
    context={
        'form':form,
        'purpose':purpose,

    }
    return render(request, "tracker/purposeedit.html" ,context)

@login_required(login_url='login')
def deletepurpose(request, pk):

    purpose = Purpose.objects.get(id=pk)
    form = PurposeForm(instance=purpose)

    if request.method == 'POST':

        purpose.delete()
        return redirect('/list')
 
    context={
        'form':form,
        'purpose':purpose
    }
    return render(request, "tracker/purposedelete.html" ,context)




# NETWORTH

@login_required(login_url='login')
def addnetworth(request):
    
    form = NetworthForm(request.POST)

    if request.method == 'POST':
        #print('printpost',request.POST)
        form = NetworthForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/list')
 
    context = {'form' : form }
    
    return render(request, "tracker/netadd.html" ,context)

@login_required(login_url='login')
def editnetworth(request, pk):

    networth = Networth.objects.get(id=pk)
    form = NetworthForm(instance=networth)

    if request.method == 'POST':

        #print('hey', request.POST)
        form = NetworthForm(request.POST, instance=networth)
        if form.is_valid():
            form.save()
            return redirect('/list')
 
    context={
        'form':form,
        'purpose':networth,

    }
    return render(request, "tracker/netedit.html" ,context)




# FixedCost
@login_required(login_url='login')
def addFixedCost(request):
    
    form = FixedCostForm(request.POST)

    if request.method == 'POST':
        #print('printpost',request.POST)
        form = FixedCostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/list')
 
    context = {'form' : form }
    
    return render(request, "tracker/FixedCostAdd.html" ,context)

@login_required(login_url='login')
def editFixedCost(request, pk):

    purpose = FixedCost.objects.get(id=pk)
    form = FixedCostForm(instance=purpose)

    if request.method == 'POST':

        #print('hey', request.POST)
        form = FixedCostForm(request.POST, instance=purpose)
        if form.is_valid():
            form.save()
            return redirect('/list')
 
    context={
        'form':form,
        'purpose':purpose,

    }
    return render(request, "tracker/FixedCostEdit.html" ,context)

@login_required(login_url='login')
def deleteFixedCost(request, pk):

    purpose = FixedCost.objects.get(id=pk)
    form = FixedCostForm(instance=purpose)

    if request.method == 'POST':

        purpose.delete()
        return redirect('/list')
 
    context={
        'form':form,
        'purpose':purpose
    }
    return render(request, "tracker/FixedCostDelete.html" ,context)











