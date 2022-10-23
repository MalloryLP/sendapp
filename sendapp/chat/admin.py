from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.PublicKey)

#python manage.py migrate --run-syncdb   