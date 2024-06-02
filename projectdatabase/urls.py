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
    path('AdninLoginPage/',views.login,name="login"),
    # path('AdninLoginPage/',views.AdninLoginPage,name="AdninLoginPage"),
    path('AddNewProject/',views.addNewProject,name="AddNewProject"),
    path('ContactMe/',views.ContactMe,name="ContactMe"),
]

