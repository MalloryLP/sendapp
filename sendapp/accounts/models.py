from django.db import models

# Create your models here.

class PublicKey(models.Model):
    owner = models.TextField()
    pub = models.TextField()

class PrivateKey(models.Model):
    owner = models.TextField()
    pri = models.TextField()
