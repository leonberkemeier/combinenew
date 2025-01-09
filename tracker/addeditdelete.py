from tracker.models import *
from tracker.forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


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


# EXPENSES
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




#NETWORTH

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


# PURPOSE

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


# FIXEDCOSTS
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