import json
import websockets
from utilities.api import Api

class WebsocketService:
    def __init__(self):
        self.is_connected = False
        self.session_id = None

    # Connect with the twitch websocket
    async def connect(self, token, client_id, broadcaster_id):
        uri = 'wss://eventsub.wss.twitch.tv/ws'

        async with websockets.connect(uri) as websocket:
            welcome_message = await websocket.recv()
            data = json.loads(welcome_message)

            if data.get('payload'):
                print("Twitch websocket connection successful.")
                self.session_id = data['payload']['session']['id']
                self.is_connected = True

            await self.get_subscriptions(token, client_id, broadcaster_id)
            await self.event_handler(websocket)

    # handler the messages received from the twitch websocket
    async def event_handler(self, websocket):
        while True:
            try:
                message = await websocket.recv()
                event_data = json.loads(message)
                meta_data = event_data.get('metadata')

                if meta_data.get('message_type') == 'notification':
                    print(event_data)

            except websockets.ConnectionClosed as e:
                print(f"Conexión cerrada: {e}")

    # Create a event subscriptions from twich
    async def get_subscriptions(self, token, client_id, broadcaster_id):
        if not self.is_connected: return

        api = Api(token, client_id)
        api.get_subscription(broadcaster_id, self.session_id, 'stream.online')
        api.get_subscription(broadcaster_id, self.session_id, 'stream.offline')