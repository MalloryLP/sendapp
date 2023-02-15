from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from accounts.forms import CustomUserRegisterForm

from accounts.models import PrivateKey, PublicKey

import json, time

# Create your views here.

class Register(View):

    def get(self, request):
        form = CustomUserRegisterForm()

        return render(request, 'accounts/register.html', context={'form': form})

    def post(self, request):
        form = CustomUserRegisterForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)

            return redirect('gen')

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
            return render(request, 'accounts/login.html', context={"login_error" : "Nom d'utilisateur ou mot de passe incorrect."})

class KeyGen(View):
    def get(self, request):
        return render(request, 'accounts/key_gen.html')
    
    def post(self, request):
        pass

class EncryptionKey(View):

    def isTheUserOK(user):
        if PublicKey.objects.get(owner=user).pub in "no_key":
            if PrivateKey.objects.get(owner=user).pri in"no_key":
                return True
        return False

    def get(self, request):

        print(request.headers["User"])

        if PublicKey.objects.filter(owner=request.headers["User"]).exists():
                obj1 = PublicKey.objects.get(owner = request.headers["User"])
                if PrivateKey.objects.filter(owner=request.headers["User"]).exists():
                    obj2 = PrivateKey.objects.get(owner = request.headers["User"])
                    if PublicKey.objects.filter(owner=request.headers["Referer"].split("/")[-2]).exists():
                        obj3 = PublicKey.objects.get(owner = request.headers["Referer"].split("/")[-2])
                        if PrivateKey.objects.filter(owner=request.headers["Referer"].split("/")[-2]).exists():
                            obj4 = PrivateKey.objects.get(owner = request.headers["Referer"].split("/")[-2])

                            return JsonResponse(
                                {"user": {
                                    "name": obj1.owner,
                                    "UserPublicKey": obj1.pub,
                                    "UserPrivateKey": obj2.pri
                                }, "friend": {
                                    "name": obj3.owner,
                                    "FriendPublicKey": obj3.pub,
                                    "FriendPrivateKey": obj4.pri
                                }})
                                
        return JsonResponse({'publicKey': None, 'privateKey': None})

    def post(self, request):

        body = json.loads(request.body.decode('utf-8'))
        owner = body["user"]
        pub = body["publicKey"]
        pri = body["privateKey"]

        if PublicKey.objects.filter(owner=owner).exists():
            print("Public key updated !")
            obj, created = PublicKey.objects.update_or_create(owner = owner, defaults={"pub": pub})
        else:
            print("Public key created !")
            publicKey = PublicKey()
            
            publicKey.owner = owner
            publicKey.pub = pub
            publicKey.save()

        if PrivateKey.objects.filter(owner=owner).exists():
            print("Private key updated !")
            obj, created = PrivateKey.objects.update_or_create(owner = owner, defaults={"pri": pri})
        else:
            print("Private key created !")
            privatekey = PrivateKey()
            
            privatekey.owner = owner
            privatekey.pri = pri
            privatekey.save()

        return render(request, 'chat/friendsnav.html')