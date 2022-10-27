from enum import unique
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.

class PublicKey(models.Model):
    owner = models.TextField()
    value = models.TextField()