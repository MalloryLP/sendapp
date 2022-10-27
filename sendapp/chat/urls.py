from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from chat import views

urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('api/', views.EncryptionKey.as_view(), name='api'),
]