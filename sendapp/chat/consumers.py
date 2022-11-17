import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatModel
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer

class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        user_id = self.scope['user'].id
        friend_id = self.scope['url_route']['kwargs']['id']
        
        if int(user_id) > int(friend_id):
            self.room_name = f'{user_id}-{friend_id}'
        else:
            self.room_name = f'{friend_id}-{user_id}'
        
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
