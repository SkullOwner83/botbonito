import flet as ft
from .pages.home import HomePage
from .pages.validation import ValidationPage
from .pages.commands import CommandsPage
from .pages.moderation import ModerationPage
from .pages.configuration import ConfigurationPage

class Routes:
    def __init__(self, page: ft.Page):
        self.page = page
        self.home_page = HomePage(page)
        self.validation_page = ValidationPage(page)
        self.commands_page = CommandsPage(page)
        self.moderation_page = ModerationPage(page)
        self.configuration_page = ConfigurationPage(page)
    
    def route_change(self, e) -> None:
        self.page.views.clear()

        if self.page.route == "/": self.page.views.append(self.home_page.get_view())
        elif self.page.route == "/validation": self.page.views.append(self.validation_page.get_view())
        elif self.page.route == "/commands": self.page.views.append(self.commands_page.get_view())
        elif self.page.route == "/moderation": self.page.views.append(self.moderation_page.get_view())
        elif self.page.route == "/configuration": self.page.views.append(self.configuration_page.get_view())

        self.page.update()
    
    def view_pop(self, e: ft.ViewPopEvent) -> None:
        self.page.views.pop()
        top_view: ft.View = self.page.views[-1]
        self.page.route = top_view.route
    
    def goto(self, page: str = '/') -> None:
        self.page.go(page)