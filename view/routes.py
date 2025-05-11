import flet as ft
from .pages.home import HomePage
from .pages.validation import ValidationPage
from .pages.commands import CommandsPage
from .pages.moderation import ModerationPage
from .pages.configuration import ConfigurationPage


class RouteHandler:
    def __init__(self, page: ft.Page, bot_services):
        self.page = page
        self.bot_services = bot_services
    
    def route_change(self, e) -> None:
        self.page.views.clear()
        
        match(self.page.route):
            case "/": self.page.views.append(HomePage(self.page))
            case "/validation": self.page.views.append(ValidationPage(self.page, self.bot_services))
            case "/commands": self.page.views.append(CommandsPage(self.page))
            case "/moderation": self.page.views.append(ModerationPage(self.page))
            case "/configuration": self.page.views.append(ConfigurationPage(self.page))
            case _: self.page.views.append(HomePage(self.page))

        self.page.update()
    
    def view_pop(self, e: ft.ViewPopEvent) -> None:
        self.page.views[1].can_pop
        self.page.views.pop()
        top_view: ft.View = self.page.views[-1]
        self.page.route = top_view.route
    
    def goto(self, page: str = '/') -> None:
        self.page.go(page)