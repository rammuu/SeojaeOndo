from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    nickname = models.CharField(max_length=50, unique=True)
    favorite_categories = models.JSONField(default=list)

    REQUIRED_FIELDS = ['email', 'name', 'phone_number', 'nickname']
