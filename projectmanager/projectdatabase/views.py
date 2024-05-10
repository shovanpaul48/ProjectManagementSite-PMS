from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Project
from .forms import ProjectForm
import os


from django.db.models import Q

def index(request):
    projects = Project.objects.all()
    selected_filter = request.POST.get('filter') if request.method == 'POST' else 'all'  # Default to 'all' if no filter selected
    if selected_filter != 'all':
        # Filter projects based on case-insensitive substring matching
        projects = Project.objects.filter(Q(tags__icontains=selected_filter))
    return render(request, "index.html", {"projects": projects, "selected_filter": selected_filter})


# def home(request):
#     projects = Project.objects.all()

#     return render(request,"index.html", {"projects":projects})


from django.shortcuts import render
from .models import Project

def addNewProject(request):
    if request.method == "POST":
        project_title = request.POST.get("project_title")
        tags = request.POST.get("tags")
        description = request.POST.get("description")
        links = request.POST.get("links")
        
        # Handle file upload
        image = request.FILES.get("images")

        if image:
            img_file_path = image.name
            project = Project.objects.create(
                title=project_title,
                tags=tags,
                description=description,
                links=links,
                imgs=img_file_path  # Save the file path to the Project object
            )
            # Save the uploaded image to the specified path
            project.imgs.save(img_file_path, image)

        msg = "Project Added"
        return render(request, "addNewProject.html", {'MSG': msg })
    else:
        return render(request, "addNewProject.html")
