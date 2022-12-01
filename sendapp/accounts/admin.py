from django.contrib import admin

from accounts.models import PublicKey, PrivateKey

# Register your models here.

admin.site.register(PublicKey)
admin.site.register(PrivateKey)
