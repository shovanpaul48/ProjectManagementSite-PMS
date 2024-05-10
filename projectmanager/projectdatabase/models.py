from django.db import models

# Create your models here.
class Project(models.Model):
    title =  models.CharField(max_length=200)
    tags = models.CharField(max_length=100)
    description = models.TextField()
    links = models.CharField(max_length=300)
    imgs = models.ImageField(upload_to='pics')