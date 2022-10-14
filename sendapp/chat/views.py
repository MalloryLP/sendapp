from django.shortcuts import render
from django.views import View
from . import models

# Create your views here.

class Login(View):

    def get(self, request):
        return render(request, template_name="chat/login.html")

    def post(self, request):
        username = request.POST.get("username", False)
        password = request.POST.get("password", False)
        return render(request, "chat/home.html", {"username": username, "password": password})

class Register(View):

    def get(self, request):
        return render(request, template_name="chat/register.html")

    def post(self, request):
        user = models.User()
        user.username = request.POST.get("username", False)
        user.first_name = request.POST.get("first_name", False)
        user.last_name = request.POST.get("last_name", False)
        user.email = request.POST.get("email", False)
        user.password = request.POST.get("password", False)
        user.save()
        return render(request, template_name="chat/register.html")