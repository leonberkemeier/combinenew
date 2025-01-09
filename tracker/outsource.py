from tracker.models import *
from datetime import date,datetime
import datetime as dt
from django.db.models import Sum


def rowprint(x):
    print(x)
    print(x)


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
    
    taxincome=income.filter(tax=1)  
    ntaxincome=income.filter(tax=0)
    
    if not taxincome:
        taxincome = 0
        taxincomesum = 0
    else:
        taxincomesum=taxincome.aggregate(Sum('income')).get('income__sum')
        incomesum=income.aggregate(Sum('income')).get('income__sum') 

    if not ntaxincome:       
        ntaxincome = 0
        ntaxincomesum = 0
    else:
        ntaxincomesum=ntaxincome.aggregate(Sum('income')).get('income__sum')
  
    incomesum = taxincomesum+ntaxincomesum

    if expenses == None:
        expenses = 0
    else:
        expensessum = expenses.aggregate(Sum('amount')).get('amount__sum')
    
    
    return (expenses,expensessum, income, incomesum, month, year, taxincomesum, ntaxincomesum)

def sumfixedcost():
    sumfixedcosts=0
    fixedCosts = FixedCost.objects.all()
    for i in range(len(fixedCosts)):
        sumfixedcosts += fixedCosts[i].amount
    return(sumfixedcosts)

def taxrates(request):
    expenses,expensessum,income, incomesum, month, year, taxincomesum, ntaxincomesum= datefilter(request)
    if taxincomesum <1300:  
        LS = 0
    else:
        LS = 15
    # LS =0
    KS=f"{4:.2f}"
    RV=f"{9.3:.2f}"
    KV=f"{8.3:.2f}"
    AV=f"{1.3:.2f}"
    PV=f"{2.3:.2f}"

    #Resulting Tax
    LSA=f"{incomesum*float(LS) /100:.2f}"
    KSA=f"{incomesum*float(KS) /100:.2f}"
    RVA=f"{incomesum*float(RV) /100:.2f}"
    KVA=f"{incomesum*float(KV) /100:.2f}"
    AVA=f"{incomesum*float(AV) /100:.2f}"
    PVA=f"{incomesum*float(PV) /100:.2f}"
    SummeAbgaben=f"{float(LS)+float(KSA)+float(RVA)+float(KVA)+float(AVA)+float(PVA):.2f}"

    posttax=taxincomesum - float(SummeAbgaben)
    return(posttax, SummeAbgaben,LS,KS,RV,KV,AV,PV,LSA,KSA,RVA,KVA,AVA,PVA)


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

def netfilter(n):
    # print(n)
    nf = n.filter(balance=222)
    # print(nf)
    return nf

