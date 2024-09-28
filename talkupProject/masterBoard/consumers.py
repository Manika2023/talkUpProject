import json
from channels.generic.websocket import AsyncWebsocketConsumer

class MasterBoardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'masterboard_room'  # Room name for the collaboration
        self.room_group_name = 'masterboard'  # Group name for broadcasting messages

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name  # Use channel_name to uniquely identify the connection
        )
        
        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name  # Use channel_name for unique identification
        ) 

    async def receive(self, text_data):
        # Parse incoming data as JSON
        data = json.loads(text_data)

        # Handle text messages
        if 'message' in data:
            await self.handle_message(data['message'])
        elif 'draw_action' in data:
            await self.handle_draw_action(data['draw_action'])
        else:
            # Handle unexpected input
            print("Received unexpected data:", data)

    async def handle_message(self, message):
        """
        Broadcasts a message to all clients in the room group.

        Args:
            message (str): The message to send.
        """
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'board_message',
                'message': message
            }
        )    

    async def handle_draw_action(self, draw_action):
        """
        Broadcasts a drawing action to all clients in the room group.

        Args:
            draw_action (dict): The drawing action data.
        """
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'board_draw',
                'draw_action': draw_action
            }
        )

    async def board_message(self, event):
        """
        Sends a message to the WebSocket client.

        Args:
            event (dict): The event containing the message.
        """
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def board_draw(self, event):
        """
        Sends a drawing action to the WebSocket client.

        Args:
            event (dict): The event containing the drawing action.
        """
        draw_action = event['draw_action']
        await self.send(text_data=json.dumps({
            'draw_action': draw_action
        }))
