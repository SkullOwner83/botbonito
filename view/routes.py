import flet as ft
from .pages.home import HomePage
from .pages.commands import CommandsPage
from .pages.moderation import ModerationPage
from .pages.configuration import ConfigurationPage
from services import *

class RouteHandler:
    def __init__(self, page: ft.Page, botconfig: dict, bot_services: BotService, session_service: SessionService, websocket_service: WebsocketService):
        self.page = page
        self.botconfig = botconfig
        self.bot_services = bot_services
        self.session_service = session_service
        self.websocket_service = websocket_service
    
    def route_change(self, e) -> None:
        self.page.views.clear()
        
        match(self.page.route):
            case "/home": self.page.views.append(HomePage(self.page, self.botconfig, self.session_service, self.websocket_service))
            case "/commands": self.page.views.append(CommandsPage(self.page, self.botconfig, self.session_service, self.websocket_service))
            case "/moderation": self.page.views.append(ModerationPage(self.page, self.botconfig, self.session_service, self.websocket_service))
            case "/configuration": self.page.views.append(ConfigurationPage(self.page, self.botconfig, self.session_service, self.websocket_service))
            case _: self.page.views.append(HomePage(self.page, self.botconfig, self.session_service, self.websocket_service))

        self.page.update()
    
    def view_pop(self, e: ft.ViewPopEvent) -> None:
        self.page.views[1].can_pop
        self.page.views.pop()
        top_view: ft.View = self.page.views[-1]
        self.page.route = top_view.route
    
    def goto(self, page: str = '/') -> None:
        self.page.go(page)