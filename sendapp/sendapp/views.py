from traceback import print_tb
from django.views import View
from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer

import json

User = get_user_model()

channel_layer = get_channel_layer()

class Home(View):

    def get(self, request):
        users = User.objects.exclude(username=request.user.username)
        return render(request, 'home/infos.html', context={'users': users})

    def post(self, request):
        pass
