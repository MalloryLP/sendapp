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
        user_id = request.user.id
        friend_id = User.objects.get(username=username).id

        if user_id > friend_id:
            thread_name = f'chat_{user_id}-{friend_id}'
        else:
            thread_name = f'chat_{friend_id}-{user_id}'

        message_objs = ChatModel.objects.filter(thread_name=thread_name)

        senders = {}
        send_messg = []
        for i, mesg in enumerate(message_objs):
            user_obj_temp = User.objects.get(id=mesg.sender)
            senders[user_obj_temp.id] = f"{user_obj_temp.username}"
            #send_messg.append([f"{mesg.sender}", f"{mesg.message}", mesg.timestamp])
            send_messg.append([f"{senders[user_obj_temp.id]}", f"{mesg.message}"])        

        users = User.objects.exclude(username=request.user.username)
        return render(request, 'chat/chat.html', context={'requested_user_id' : f"{friend_id}" ,'users': users, 'messages' : send_messg, 'friend' : username, 'count' : len(send_messg)})


    def post(self, request):
        pass