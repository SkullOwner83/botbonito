import inspect
import socket
import asyncio
import json
import websockets
from utilities.api import Api

class WebsocketService:
    def __init__(self):
        self.is_connected = False
        self.session_id = None
        self.stream_online_callback = []
        self.stream_offline_callback = []
        self.channel_follower_callback =[]
        self.channel_subscription_callback = []
        self.channel_raid_callback = []

    # Connect with the twitch websocket for Event Sub
    async def connect(self, token, client_id, broadcaster_id):
        uri = 'wss://eventsub.wss.twitch.tv/ws'
        retry_delay = 5

        while True:
            try:
                async with websockets.connect(uri) as websocket:
                    welcome_message = await websocket.recv()
                    data = json.loads(welcome_message)

                    if data.get('payload'):
                        print("Twitch websocket connection successful.")
                        self.session_id = data['payload']['session']['id']
                        self.is_connected = True

                    await self.create_subscriptions(token, client_id, broadcaster_id)
                    await self.event_handler(websocket)
            except (socket.gaierror, websockets.exceptions.InvalidURI, ConnectionRefusedError) as error:
                print(f"Connection with the websocket failed: {error}")
            except websockets.ConnectionClosedError as error:
                print(f"Twitch websocket connection disconected: {error}")
            except Exception as error:
                print(f"An error occurred: {error}")
                
            await asyncio.sleep(retry_delay)

    # handler the messages received from the twitch websocket
    async def event_handler(self, websocket) -> None:
        while True:
            try:
                message = await websocket.recv()
                event_data = json.loads(message)
                payload = event_data.get('payload')
                meta_data = event_data.get('metadata')
                subscription_type = meta_data.get('subscription_type')

                if meta_data.get('message_type') == 'notification':
                    if subscription_type == 'stream.online': await self.on_stream_online(payload)
                    if subscription_type == 'stream.offline': await self.on_stream_offline(payload)
                    if subscription_type == 'channel.follow': await self.on_channel_follower(payload)
                    if subscription_type == 'channel.subscribe': await self.on_channel_subscription(payload)
                    if subscription_type == 'channel.raid': await self.on_channel_raid(payload)

            except websockets.ConnectionClosed as e:
                print(f"Twitch websocket connection disconected: {e}")
                self.is_connected = False
                break

    # Create a event subscriptions from twich
    async def create_subscriptions(self, token, client_id, broadcaster_id) -> None:
        if not self.is_connected: return

        api = Api(token, client_id)
        data = api.get_subscriptions()
        
        for event_sub in data:
            api.delete_subscription(event_sub['id'])
        
        api.create_subscription(broadcaster_id, self.session_id, 'stream.online')
        api.create_subscription(broadcaster_id, self.session_id, 'stream.offline')
        api.create_subscription(broadcaster_id, self.session_id, 'channel.follow', version=2)
        api.create_subscription(broadcaster_id, self.session_id, 'channel.subscribe')

    async def run_callback(self, callback: callable, payload):
        if inspect.iscoroutinefunction(callback):
            await callback(payload)
        else:
            callback(payload)

    async def on_stream_online(self, payload: dict):
        for callback in self.stream_online_callback:
            await self.run_callback(callback, payload)
    
    async def on_stream_offline(self, payload: dict):
        for callback in self.stream_offline_callback:
            await self.run_callback(callback, payload)

    async def on_channel_follower(self, payload: dict):
        for callback in self.channel_follower_callback:
            await self.run_callback(callback, payload)
    
    async def on_channel_subscription(self, payload: dict):
        for callback in self.channel_subscription_callback:
            await self.run_callback(callback, payload)

    async def on_channel_raid(self, payload: dict):
        for callback in self.channel_raid_callback:
            await self.run_callback(callback, payload)