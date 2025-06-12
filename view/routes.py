import flet as ft
from .pages.home import HomePage
from .pages.commands import CommandsPage
from .pages.moderation import ModerationPage
from .pages.configuration import ConfigurationPage
from services import *

class RouteHandler:
    def __init__(self, page: ft.Page, botconfig: dict):
        self.page = page
        self.botconfig = botconfig
    
    def route_change(self, e) -> None:
        self.page.views.clear()
        
        match(self.page.route):
            case "/home": self.page.views.append(HomePage(self.page, self.botconfig))
            case "/commands": self.page.views.append(CommandsPage(self.page, self.botconfig))
            case "/moderation": self.page.views.append(ModerationPage(self.page, self.botconfig))
            case "/configuration": self.page.views.append(ConfigurationPage(self.page, self.botconfig))
            case _: self.page.views.append(HomePage(self.page, self.botconfig))

        self.page.update()
    
    def view_pop(self, e: ft.ViewPopEvent) -> None:
        self.page.views[1].can_pop
        self.page.views.pop()
        top_view: ft.View = self.page.views[-1]
        self.page.route = top_view.route
    
    def goto(self, page: str = '/') -> None:
        self.page.go(page)