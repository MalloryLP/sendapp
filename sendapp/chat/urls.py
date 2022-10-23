from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from chat import views

urlpatterns = [
    path('home/', views.Home.as_view(), name='home'),
    path('register/', views.Register.as_view(), name='register'),
  
    path('login/', auth_views.LoginView.as_view(template_name='chat/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='chat/logout.html'), name='logout'),

    path('api/', views.EncryptionKey.as_view(), name='api'),
]