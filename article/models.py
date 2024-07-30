from django.db import models
from django.conf import settings
# Create your models here.

class ArticleModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author= models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)