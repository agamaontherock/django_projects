import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['topic_id']
        self.user = self.scope['user']
        self.room_group_name = f'chat_{self.id}'
        # join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        # accept connection
        await self.accept()
        
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        # receive message from WebSocket
        
    async def persist_message(self, message):
        await Message.objects.acreate(
            topic_id=self.id,
            user=self.user,
            message=message
        )
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        # send message to WebSocket
        # self.send(text_data=json.dumps({'message': message}))
        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type': 'chat_message',
            'message': message,
            'user': self.user.username,
            'sent_on': now.strftime("%Y-%m-%d %H:%M:%S")
            }
        )
        await self.persist_message(message)
    
    # receive message from room group
    async def chat_message(self, event):
    # send message to WebSocket
        await self.send(text_data=json.dumps(event))