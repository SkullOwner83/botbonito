import flet as ft

from models.appconfig import AppConfig
from .pages.home import HomePage
from .pages.commands import CommandsPage
from .pages.moderation import ModerationPage
from .pages.configuration import ConfigurationPage
from services import *

class RouteHandler:
    def __init__(self, page: ft.Page, app_config: AppConfig):
        self.page = page
        self.app_config = app_config
    
    def route_change(self, e) -> None:
        self.page.views.clear()
        
        match(self.page.route):
            case "/home": self.page.views.append(HomePage(self.page, self.app_config))
            case "/commands": self.page.views.append(CommandsPage(self.page, self.app_config))
            case "/moderation": self.page.views.append(ModerationPage(self.page, self.app_config))
            case "/configuration": self.page.views.append(ConfigurationPage(self.page, self.app_config))
            case _: self.page.views.append(HomePage(self.page, self.app_config))

        self.page.update()
    
    def view_pop(self, e: ft.ViewPopEvent) -> None:
        self.page.views[1].can_pop
        self.page.views.pop()
        top_view: ft.View = self.page.views[-1]
        self.page.route = top_view.route
    
    def goto(self, page: str = '/') -> None:
        self.page.go(page)