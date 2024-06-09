from django.urls import path 
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

# urlpatterns = [
#     path('',views.home,name='home'),
#     path('addNewProject',views.addNewProject,name='addNewProject')
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('', views.index2, name='index2'),
    path('AdninLoginPage/',views.login,name="login"),
    # path('AdninLoginPage/',views.AdninLoginPage,name="AdninLoginPage"),
    # path('ProjectsPage/',views.ProjectsPage,name="ProjectsPage"),
    path('ProjectsPage/<int:project_id>/', views.ProjectsPage, name='ProjectsPage'),
    path('AddNewProject/',views.addNewProject,name="AddNewProject"),
    path('ContactMe/',views.ContactMe,name="ContactMe"),
    path('CURD/',views.CURD,name="CURD"),
    path('update_project/', views.update_project, name='update_project'),
    path('', views.project_management, name='project_management'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('delete_selected_projects/', views.delete_selected_projects, name='delete_selected_projects'),


]

