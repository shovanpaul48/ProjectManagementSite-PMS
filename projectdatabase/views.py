from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Project
from .forms import ProjectForm
import os
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages


def index(request):
    if request.method == 'POST':
        selected_filter = request.POST.get('filter', 'all')
        if selected_filter == 'all':
            projects = Project.objects.all()
        else:
            projects = Project.objects.filter(tags__icontains=selected_filter)
        return render(request, 'index.html', {'projects': projects, 'selected_filter': selected_filter})

    projects = Project.objects.all()
    return render(request, 'index.html', {'projects': projects, 'selected_filter': 'all'})

def addNewProject(request):
    if request.method == "POST":
        project_title = request.POST.get("project_title")
        tags = request.POST.get("tags")
        description = request.POST.get("description")
        links = request.POST.get("links")
        priority = request.POST.get('priority')
        image = request.FILES.get("images")

        if image:
            img_file_path = image.name
            project = Project.objects.create(
                title=project_title,
                tags=tags,
                description=description,
                links=links,
                imgs=img_file_path,  # Save the file path to the Project object
                priority = priority
            )
            # Save the uploaded image to the specified path
            project.imgs.save(img_file_path, image)

        msg = "Project Added"
        return render(request, "addNewProject.html", {'MSG': msg })
    else:
        return render(request, "addNewProject.html")
'''
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
            # login(request, user)
        if username=="shovanpaul48" and password=="2024": 
            # return redirect('index', {'Admin mode'})  # Replace 'home' with your desired redirect URL
            return redirect('AddNewProject')
        else:
            messages.error(request, 'Invalid login credentials')
    return render(request, 'Admin_Login.html')
'''
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Simulated authentication for demonstration purposes
        if username == "shovanpaul48" and password == "2024": 
            # messages.success(request, 'Successful login')
            return redirect('AddNewProject')
            
        else:
            msg="Invalid login credentials"
            return render(request, "Admin_Login.html", {'MSG': msg })
            # messages.error(request, 'Invalid login credentials')
    
    return render(request, 'Admin_Login.html')


def ContactMe(request):
    return render(request, 'ContactPage.html')