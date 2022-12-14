from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('gen/', views.KeyGen.as_view(), name='gen'),
    path('api/', views.EncryptionKey.as_view(), name='api'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]