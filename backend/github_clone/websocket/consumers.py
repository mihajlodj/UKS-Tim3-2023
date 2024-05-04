import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('CONNECT')
        username = self.scope['url_route']['kwargs']['username']
        self.group_name = username
        print(username)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        print('DISCONNECT')
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        print('SEND')
        await self.send(text_data=json.dumps({ 'message': event['message'] }))
