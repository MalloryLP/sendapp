from django.views import View
from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model

import json

from chat.models import PublicKey

User = get_user_model()

class Home(View):

    def get(self, request):
        #print("first id", User.objects.get(username='nadir.ziani').id)
        #print("second id", request.user.id)
        users = User.objects.exclude(username=request.user.username)
        print(users)
        return render(request, 'chat/home.html', context={'users': users})

    def post(self, request):
        return render(request, 'chat/home.html')

class EncryptionKey(View):

    def get(self, request):
        pass

    def post(self, request):

        body = json.loads(request.body.decode('utf-8'))
        owner = body["user"]
        value = body["publicKey"]

        if PublicKey.objects.filter(owner=owner).exists():
            print("Public key updated !")
            obj, created = PublicKey.objects.update_or_create(owner = owner, defaults={"value": value})
        else:
            print("Public key created !")
            publicKey = PublicKey()
            
            publicKey.owner = owner
            publicKey.value = value
            publicKey.save()

        

        return render(request, 'chat/home.html')