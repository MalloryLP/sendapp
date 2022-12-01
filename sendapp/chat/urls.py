from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from chat import views

urlpatterns = [
    path('chat/', views.Home.as_view(), name='chat'),
    path('chat/<str:username>/', views.Chat.as_view(), name='friendchat')
]