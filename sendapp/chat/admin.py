from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.PublicKey)
admin.site.register(models.ChatModel)

#python manage.py migrate --run-syncdb   