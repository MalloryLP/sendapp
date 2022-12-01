from django.contrib import admin
from chat.models import ChatModel

# Register your models here.

admin.site.register(ChatModel)

#python manage.py migrate --run-syncdb   