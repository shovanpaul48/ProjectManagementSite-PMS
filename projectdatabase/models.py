# from django.db import models

# # Create your models here.
# class Project(models.Model):
#     title =  models.CharField(max_length=200)
#     tags = models.CharField(max_length=100)
#     description = models.TextField()
#     links = models.CharField(max_length=300)
#     imgs = models.ImageField(upload_to='pics')

from django.db import models


class Project(models.Model):
    PRIORITY_CHOICES = [
        ('H', 'High'),
        ('M', 'Medium'),
        ('L', 'Low'),
    ]

    title = models.CharField(max_length=200)
    tags = models.CharField(max_length=100)
    description = models.TextField()
    links = models.CharField(max_length=300)
    imgs = models.ImageField(upload_to='pics')
    priority = models.CharField(max_length=1, choices=PRIORITY_CHOICES, default='M')
    # image_url = models.URLField(max_length=200, blank=True, null=True)
