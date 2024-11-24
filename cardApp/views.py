from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import ProjectCategory, Project
from .forms import ProjectCategoryForm, ProjectForm

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
    projects = Project.objects.all()

    context={
        'projectcategories': projectcategories,
        'projects': projects
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
