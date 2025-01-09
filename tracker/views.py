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

from tracker.outsource import *
from tracker.addeditdelete import *

@login_required(login_url='login')
def tracker(request):
    expenses,expensessum,income, incomesum, month, year, taxincomesum, ntaxincomesum = datefilter(request)
    posttax, SummeAbgaben,LS,KS,RV,KV,AV,PV,LSA,KSA,RVA,KVA,AVA,PVA=taxrates(request)
    if year is not None and month is not None:
        days = calendar.monthrange(int(year),int(month))[1]

    current_time = dt.datetime.now()
    current_day = current_time.day

    #Average Income
    postTaxFixedCosts = posttax-sumfixedcost()
    avgincome = round(postTaxFixedCosts/days, 2)
    
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
    rel_balance=0
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

    el = expenseList(expenses)






    addincomeform = IncomeForm(request.POST)
    addexpenseform = ExpensesForm(request.POST)

    context={
        'income':incomesum,
        'totalexpenses':totalexpenses,
        # 'assets':assets,
        # 'balance':balance,

        # 'networth':networth,

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
  
    expenses,expensessum, income, incomesum, month, year, taxincomesum, ntaxincomesum= datefilter(request)

    
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

    expenses,expensessum,income, incomesum, month, year, taxincomesum, ntaxincomesum= datefilter(request) 
    posttax, SummeAbgaben,LS,KS,RV,KV,AV,PV,LSA,KSA,RVA,KVA,AVA,PVA=taxrates(request)

    totalincome=posttax+ntaxincomesum

    #Expensese
    sumExpenses=0
    purposelist = Purpose.objects.all()
    for purposeitem in purposelist:
        summeexpenses = expenses.filter(purpose=purposeitem).aggregate(Sum('amount')).get('amount__sum')
        if summeexpenses == None:
            summeexpenses = 0
            purposeitem.percent = 0
            purposeitem.expense = summeexpenses
        else:
            purposeitem.expense = summeexpenses
            purposeitem.percent = f"{summeexpenses / posttax*100 :.2f}"
        sumExpenses+=summeexpenses
    
    #FixedCosts
    sumfixedcosts=sumfixedcost() 

    fixedCosts = FixedCost.objects.all()
    for fixedCost in fixedCosts:
        fixedCost.percent = f"{fixedCost.amount / posttax*100 :.2f}"

    if incomesum==0:
        sumfixedcostsrate =0
        sumcostsrate=0
    else:
        sumfixedcostsrate =f"{sumfixedcosts/posttax*100:.2f}"
        sumcostsrate = f"{sumExpenses/posttax*100:.2f}"
    
    #Sparplan
    sparplanrate = f"{10.00:.2f}"
    sparplan = incomesum/float(sparplanrate)
    fsparplan =f"{sparplan:.2f}" 
    sparplan1 = totalincome - sumExpenses -sumfixedcosts
    nosparplan = sparplan1 - sparplan

    context={
        'year':year,
        'month':month,

        'ntaxincomesum':ntaxincomesum,
        'taxincomesum':taxincomesum,
        'incomesum':incomesum,
        'expensessum':expensessum,

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
        'sumcosts':sumExpenses,
        'sumcostsrate':sumcostsrate,
        'sumfixedcosts':sumfixedcosts,
        'sumfixedcostsrate':sumfixedcostsrate,

        'sparplan':fsparplan,
        'sparplanrate':sparplanrate,
        'sparplan1':sparplan,
        'nosparplan2':nosparplan,
    }
    return render(request, 'tracker/balance.html', context)

@login_required(login_url='login')
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
