from traceback import print_tb
from django.views import View
from django.shortcuts import render, redirect

from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer

import json

from chat.models import ChatModel

User = get_user_model()

channel_layer = get_channel_layer()

class Home(View):

    def get(self, request):
        #print("first id", User.objects.get(username='nadir.ziani').id)
        #print("second id", request.user.id)
        users = User.objects.exclude(username=request.user.username)
        return render(request, 'chat/friendsnav.html', context={'users': users})

    def post(self, request):
        pass

class Chat(View):

    def get(self, request, username):
        session_user_id = request.user.id
        requested_user_id = User.objects.get(username=username).id

        if session_user_id > requested_user_id:
            thread_name = f'chat_{session_user_id}-{requested_user_id}'
        else:
            thread_name = f'chat_{requested_user_id}-{session_user_id}'

        print(thread_name)

        message_objs = ChatModel.objects.filter(thread_name=thread_name)
        senders = {}
        send_messg = []
        for i, mesg in enumerate(message_objs):
            user_obj_temp = User.objects.get(id=mesg.sender)
            senders[user_obj_temp.id] = f"{user_obj_temp.username}"
            send_messg.append([f"{mesg.sender}", f"{mesg.message}", mesg.timestamp])

        users = User.objects.exclude(username=request.user.username)
        return render(request, 'chat/chat.html', context={'requested_user_id' : f"{requested_user_id}" ,'users': users, 'messages' : send_messg, 'username' : username, 'count' : len(send_messg)})


    def post(self, request):
        pass