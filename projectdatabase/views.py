from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Project
from .forms import ProjectForm
import os
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render, redirect
from .models import Project
from cloudinary.uploader import upload

def index2(request):
    render(request,'index2.html')

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

def ProjectsPage(request,project_id):
    project = Project.objects.get(id=project_id)
    return render(request, 'Projects_Pages.html',{'project': project})



def addNewProject(request):
    if request.method == "POST":
        project_title = request.POST.get("project_title")
        tags = request.POST.get("tags")
        description = request.POST.get("description")
        links = request.POST.get("links")
        priority = request.POST.get('priority')
        image = request.FILES.get("images")

        if image:
            # Create the Project instance
            project = Project.objects.create(
                title=project_title,
                tags=tags,
                description=description,
                links=links,
                priority=priority
            )
            # Save the uploaded image to the project's imgs field
            project.imgs.save(image.name, image)
            # Now, you can access the URL of the uploaded image and store it in the project
            project.imgs = project.imgs.url
            project.save()

        msg = "Project Added"
        active_section = request.GET.get('section', 'create')  # Default to 'create' if no section is provided
        context = {
            'active_section': active_section,
            'projects': Project.objects.all(),  # Assuming you have a Project model
            'msg' : msg,
        }

        return render(request, 'CURD.html', context)
    else:
        projects = Project.objects.all()
        return render(request, 'CURD.html', {'projects': projects})

'''def addNewProject(request):
    if request.method == "POST":
        project_title = request.POST.get("project_title")
        tags = request.POST.get("tags")
        description = request.POST.get("description")
        links = request.POST.get("links")
        priority = request.POST.get('priority')
        image = request.FILES.get("images")

        if image:
            # Upload the image to Cloudinary with resizing and compression
            upload_result = cloudinary.uploader.upload(
                image,
                transformation=[
                    {'width': 800, 'height': 600, 'crop': 'limit'},  # Resize while maintaining aspect ratio
                    {'quality': 'auto'}  # Compress image
                ]
            )

            project = Project.objects.create(
                title=project_title,
                tags=tags,
                description=description,
                links=links,
                priority=priority,
                imgs=image.name,
                image_url=upload_result['secure_url']  # Use secure URL
            )
        else:
            project = Project.objects.create(
                title=project_title,
                tags=tags,
                description=description,
                links=links,
                priority=priority
            )

        msg = "Project Added"
        active_section = request.GET.get('section', 'create')  # Default to 'create' if no section is provided
        context = {
            'active_section': active_section,
            'projects': Project.objects.all(),  # Assuming you have a Project model
            'msg': msg,
        }

        return render(request, 'CURD.html', context)
    else:
        projects = Project.objects.all()
        return render(request, 'CURD.html', {'projects': projects})
'''

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Simulated authentication for demonstration purposes
        if username == "shovanpaul48" and password == "2024": 
            # messages.success(request, 'Successful login')
            return redirect('CURD')
            
        else:
            msg="Invalid login credentials"
            return render(request, "Admin_Login.html", {'MSG': msg })
            # messages.error(request, 'Invalid login credentials')
    
    return render(request, 'Admin_Login.html')


def ContactMe(request):
    return render(request, 'ContactPage.html')


def CURD(request):
    projects = Project.objects.all()
    return render(request, 'CURD.html',{'projects': projects})




from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .models import Project

def project_management(request):
    projects = Project.objects.all()
    return render(request, 'project_management.html', {'projects': projects})




"""########### DELETE #####################################
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Project
import cloudinary.uploader

def get_public_id_from_url(url):
    return url.split('/')[-1].split('.')[0]

@require_http_methods(["DELETE"])
def delete_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        if project.image_url:
            # Delete the image from Cloudinary using the public ID extracted from the URL
            public_id = get_public_id_from_url(project.image_url)
            cloudinary.uploader.destroy(public_id)
        project.delete()
        msg = str(project_id) + " DELETED"
        response_data = {'success': True, 'msg': msg}
    except Project.DoesNotExist:
        response_data = {'success': False, 'msg': 'Project not found'}
    return JsonResponse(response_data)

@require_http_methods(["POST"])
def delete_selected_projects(request):
    project_ids = request.POST.getlist('selected_projects')
    projects = Project.objects.filter(id__in=project_ids)
    for project in projects:
        if project.image_url:
            # Delete the image from Cloudinary using the public ID extracted from the URL
            public_id = get_public_id_from_url(project.image_url)
            cloudinary.uploader.destroy(public_id)
    deleted_count = projects.delete()[0]
    if deleted_count > 0:
        msg = ",".join(project_ids) + " DELETED"
        response_data = {'success': True, 'msg': msg}
    else:
        response_data = {'success': False, 'msg': 'No projects deleted'}
    return JsonResponse(response_data)

"""

def delete_image_from_cloudinary(image_url):
    # Extract the public ID from the Cloudinary URL
    public_id = image_url.split('/')[-1].split('.')[0]
    # Delete the image from Cloudinary
    cloudinary.uploader.destroy(public_id)

@require_http_methods(["DELETE"])
def delete_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
        # Delete the associated image from Cloudinary
        delete_image_from_cloudinary(project.imgs)
        # Delete the project from the database
        project.delete()
        msg = f"Project with ID {project_id} deleted"
        response_data = {'success': True, 'msg': msg}
    except Project.DoesNotExist:
        response_data = {'success': False, 'msg': 'Project not found'}
    return JsonResponse(response_data)

@require_http_methods(["POST"])
def delete_selected_projects(request):
    project_ids = request.POST.getlist('selected_projects')
    projects = Project.objects.filter(id__in=project_ids)
    for project in projects:
        # Delete the associated image from Cloudinary
        delete_image_from_cloudinary(project.imgs.url)
    deleted_count = projects.delete()[0]
    if deleted_count > 0:
        msg = f"{deleted_count} projects deleted"
        response_data = {'success': True, 'msg': msg}
    else:
        response_data = {'success': False, 'msg': 'No projects deleted'}
    return JsonResponse(response_data)

############ UPDATE #####################################
from django.views.decorators.csrf import csrf_exempt

def update_project(request):
    if request.method == 'POST':
        project_id = request.POST['project_id']
        title = request.POST['title']
        description = request.POST['description']
        tags = request.POST['tags']
        
        try:
            project = Project.objects.get(id=project_id)
            project.title = title
            project.description = description
            project.tags = tags
            project.save()
            return JsonResponse({'success': True})
        except Project.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Project not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
