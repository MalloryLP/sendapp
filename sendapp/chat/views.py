from django.shortcuts import render, redirect
from chat.form import UserRegistrationForm
from django.views import View

import json

from chat.models import PublicKey

class Home(View):

    def get(self, request):
        return render(request, 'chat/home.html')

    def post(self, request):
        return render(request, 'chat/home.html')

class Register(View):

    def get(self, request):
        form = UserRegistrationForm()
        context = {'form': form}
        return render(request, 'chat/register.html', context)

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()   
            return redirect('login')
        context = {'form': form}
        return render(request, 'chat/register.html', context)

class EncryptionKey(View):

    def get(self, request):
        pass

    def post(self, request):
        #print(request.headers)
        #print(request.body)

        body = json.loads(request.body.decode('utf-8'))
        print(body)

        publicKey = PublicKey()
        
        publicKey.owner = body["user"]
        publicKey.value = body["publicKey"]
        publicKey.save()

        return render(request, 'chat/home.html')