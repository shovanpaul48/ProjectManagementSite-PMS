# In forms.py
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'tags', 'description', 'links', 'imgs']
