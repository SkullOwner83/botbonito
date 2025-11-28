from typing import TYPE_CHECKING
from twitchio.ext import commands
from models.appconfig import AppConfig
from services.event_service import EventService
from services.service_locator import ServiceLocator
from services.websocket_service import WebsocketService
if TYPE_CHECKING: from bot.bot import Bot

class EventManager():
    def __init__(self, bot: commands.Bot, app_config: AppConfig):
        self.bot: Bot = bot
        self.events_manager: EventService = ServiceLocator.get('events')
        websocket_manager: WebsocketService = ServiceLocator.get('websocket')
        websocket_manager.stream_offline_callback.append(self.on_stream_onffline)
        websocket_manager.stream_online_callback.append(self.on_stream_online)
        websocket_manager.channel_follow_callback.append(self.on_channel_follow)
        websocket_manager.channel_subscription_callback.append(self.on_channel_subscribe)
        websocket_manager.channel_update_callback.append(self.on_channel_update)
    
    async def on_stream_onffline(self, payload: dict) -> None:
        event_config = self.events_manager.events.get('stream.offline')

        if event_config.enable:
            await self.bot.send_message(event_config.response)
        
    async def on_stream_online(self, payload: dict) -> None:
        event_config = self.events_manager.events.get('stream.online')
        data: dict = payload.get('event', {})
        started_at = data.get('started_at')
        response = event_config.response.format(started_at=started_at)

        if event_config.enable:
            await self.bot.send_message(response)

    async def on_channel_follow(self, payload: dict) -> None:
        event_config = self.events_manager.events.get('channel.follow')
        data: dict = payload.get('event', {})
        user_name = data.get('user_name')
        user_id = data.get('user_id')
        followed_at = data.get('followed_at')
        response = event_config.response.format(user=user_name, user_id=user_id, followed_at=followed_at)

        if event_config.enable:
            await self.bot.send_message(response)

    async def on_channel_subscribe(self, payload: dict) -> None:
        event_config = self.events_manager.events.get('channel.subscribe')
        data: dict = payload.get('event', {})
        user_name = data.get('user_name')
        user_id = data.get('user_id')
        followed_at = data.get('followed_at')
        response = event_config.response.format(user=user_name, user_id=user_id, followed_at=followed_at)

        if event_config.enable:
            await self.bot.send_message(response)

    async def on_channel_update(self, payload: dict) -> None:
        event_config = self.events_manager.events.get('channel.update')
        data: dict = payload.get('event', {})
        title = data.get('title')
        category = data.get('category_name')
        language = data.get('language')
        response = event_config.response.format(title=title, category=category, language=language)
        
        if event_config.enable:
            await self.bot.send_message(response)