import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatModel
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

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

    async def receive(self, text_data=None, bytes_data=None):
        print("Daphne - message received")
        data = json.loads(text_data)

        type = data['type']
        message = data['message']
        username = data['username']

        if type == "text":
            await self.save_message(username, self.room_group_name, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                }
            )
        elif type == "image":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_image',
                    'message': message,
                    'username': username,
                }
            )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        print("Daphne - " + username + " - message send using chat_message")

        await self.send(text_data=json.dumps({
            'type': 'text',
            'message': message,
            'username': username
        }))

    async def chat_image(self, event):
        message = event['message']
        username = event['username']

        print("Daphne - " + username + " - message send using chat_image")

        await self.send(text_data=json.dumps({
            'type': 'image',
            'message': message,
            'username': username
        }))

    @database_sync_to_async
    def save_message(self, username, thread_name, message):
        user_id = self.scope['user'].id
        ChatModel.objects.create(sender=user_id, message=message, thread_name=thread_name)