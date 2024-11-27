from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count

from .models import ProjectCategory, Project, Card
from .forms import ProjectCategoryForm, ProjectForm, CardForm

import random
# Create your views here.



def loginPage(request):
    
    if request.user.is_authenticated:
        
        return redirect('cards')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            context={} 
            user = authenticate(request, username=username, password = password)

            if user is not None:
                
                login(request, user)
                
                return redirect('cards')
        
            else:
                
                messages.warning(request, 'Username OR Password is Incorrect')
                return render(request, 'cards/login.html', context)

        context={} 
         
        return render(request, 'cards/login.html', context)
    
def logoutUser(request):
    logout(request)
    return redirect('/')    


@login_required(login_url='login')
def index(request):
    
    if request.user.is_superuser:
        projectcategories=ProjectCategory.objects.all()
    else:
        projectcategories =ProjectCategory.objects.filter(user=request.user.id)
    # projects = Project.objects.all()
    form1 = ProjectCategoryForm(request.POST)
    form2 = ProjectForm(request.POST)

    projects= Project.objects.annotate(Count('card'))

    for projectcategory in projectcategories:
        projectcategory.projects = Project.objects.filter(category_id=projectcategory.id).annotate(Count('card'))

    if request.method=='POST':
        form_type = request.POST.get('form_type')

    context={
        'projectcategories': projectcategories,
        'projects': projects,
        'form1':form1,
        'form2':form2

    }
    return render(request, 'cards/categories.html',context)


@login_required(login_url='login')
def addProjectCategory(request):
    # print(request.user)
    form = ProjectCategoryForm(request.POST)
    if request.method == 'POST':
        form = ProjectCategoryForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            print(request.user)
            print(request.user.id)
            project.user = request.user.id
            form.save()
            return redirect('/cards')
    context={
        'form': form
    }
    return render(request, 'cards/addProjectCategory.html',context)

@login_required(login_url='login')
def addProject(request):
    print(request.user)
    form = ProjectForm(request.POST)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user.id
            form.save()
            return redirect('/cards')
    context={
        'form': form
    }
    return render(request, 'cards/addProject.html',context)

@login_required(login_url='login')
def projects(request):
    projects=Project.objects.filter(user=request.user)
    
    context={
        'projects':projects
    }
    return render(request, 'cards/projects.html', context)


@login_required(login_url='login')
def show_project(request, *, id):
    project = Project.objects.get(id=id)
    cards = Card.objects.filter(project_id=id)
    
    # print(request.user)
    # print(request.user.id)
    # print(project.user)

    if request.user.is_superuser:
        project = Project.objects.get(id=id)
        cards = Card.objects.filter(project_id=id)
        print('hellosuperuser')
    elif request.user.id == project.user:
        project = Project.objects.get(id=id)
        cards = Card.objects.filter(project_id=id)
        print('hellouser')
    else:
        print('hellono')
        return redirect('cards')



    row_id = Project.objects.get(id=id)
    row_id = row_id.id
    print(row_id)
    form = CardForm(request.POST)
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user 
            card.project_id=row_id
            form.save()
            return redirect('/cards')
    else:
        form= CardForm()
    
    

    context={
        'project':project,
        'cards':cards,
        'form':form,
        'row_id':row_id
    }
    return render(request, 'cards/show_project.html', context)


@login_required(login_url='login')
def addCard(request, *, id):
    row_id = Project.objects.get(id=id)
    row_id = row_id.id
    
    form = CardForm(request.POST)
    if request.method == 'POST':
        form = CardForm(request.POST, request.FILES)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user.id
            card.project_id=row_id
           
            form.save()
            return redirect('/projects/{row_id}'.format(row_id=row_id))
    else:
        form= CardForm()
    context={
        'form': form
    }
    return render(request, 'cards/addCard.html',context)


@login_required(login_url='login')
def rendernextcard(request, *, id):

    cards = Card.objects.filter(project_id=id)

    try:
        after=request.GET.get('after', None)
        before=request.GET.get('before', None)
        
        if after is not None:
            print('afterisnotnone')
            card=cards.filter(id__gt=after).order_by('id')[0]
            print(cards.filter(id__gt=after))
        elif before is not None:
            print('beforeisnotnone')
            card=cards.filter(id__gt=before).order_by('id')[0]
        else:
            card=cards.order_by('id')[0]

    except IndexError:
        if len(cards) > 0:
            card = cards[0]
    except ValueError:
        if len(cards) > 0:
            card = cards[0]

    context={
        'card':card,
    }
    return render(request, 'card/modalhx.html', context =context)


@login_required(login_url='login')
def renderrndcard(request, *, id):
    cardlist = list(Card.objects.filter(project_id=id))
    random_item=random.choice(cardlist)
    card = random_item

    context ={
        'card':card,
    }
    return render(request, 'cards/modalhx.html',context=context)