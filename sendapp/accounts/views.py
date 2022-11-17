from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout

from accounts.forms import CustomUserRegisterForm

# Create your views here.

class Register(View):

    def get(self, request):
        form = CustomUserRegisterForm()
        context = {
            'form': form
        }
        return render(request, 'accounts/register.html', context=context)

    def post(self, request):
        form = CustomUserRegisterForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)

            return redirect('gen')

class KeyGen(View):
    def get(self, request):
            return render(request, 'accounts/key_gen.html')

class Login(View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request, 'accounts/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('home')
        else:
            return render(request, 'accounts/login.html')