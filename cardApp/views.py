from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count

from .models import ProjectCategory, Project, Card
from .forms import ProjectCategoryForm, ProjectForm, CardForm

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
    projectcategories =ProjectCategory.objects.all()
    # projects = Project.objects.all()

    projects= Project.objects.annotate(Count('card'))
    # print(q)
    # print(q[0].card__count)
    # print(q[1].card__count)
    # print(q[2].card__count)
    # print(q[3].card__count)

    context={
        'projectcategories': projectcategories,
        'projects': projects,

    }
    return render(request, 'cards/index.html',context)


@login_required(login_url='login')
def addProjectCategory(request):
    # print(request.user)
    form = ProjectCategoryForm(request.POST)
    if request.method == 'POST':
        form = ProjectCategoryForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user 
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
            project.user = request.user 
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

    context={
        'project':project,
        'cards':cards
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
            card.user = request.user 
            card.project_id=row_id
            form.save()
            return redirect('/cards')
    else:
        form= CardForm()
    context={
        'form': form
    }
    return render(request, 'cards/addCard.html',context)

