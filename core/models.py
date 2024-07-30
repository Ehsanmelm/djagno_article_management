from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    USER = 1
    AUTHOR = 2
    ADMIN  = 3

    ROLE_CHOICES = (
        (USER , 'User'),
        (AUTHOR , 'Author'),
        (ADMIN , 'Admin'),
    )

    role = models.IntegerField(choices=ROLE_CHOICES , default=USER)
    