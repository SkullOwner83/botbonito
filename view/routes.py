import flet as ft
from models.appconfig import AppConfig
from view.main_layout import MainLayout
from view.pages import *
from services import *

class RouteHandler:
    def __init__(self, page: ft.Page, app_config: AppConfig):
        self.page = page
        self.app_config = app_config
        self.layout = MainLayout(self.page, app_config)
        self.page.views.append(self.layout)

    def route_change(self, e) -> None:
        match self.page.route:
            case "/home": self.layout.set_content(HomePage(self.page, self.app_config))
            case "/commands": self.layout.set_content(CommandsPage(self.page, self.app_config))
            case "/moderation": self.layout.set_content(ModerationPage(self.page, self.app_config))
            case "/configuration": self.layout.set_content(ConfigurationPage(self.page, self.app_config))
            case _: self.layout.set_content(HomePage(self.page, self.app_config))

    def view_pop(self, e: ft.ViewPopEvent) -> None:
        self.page.views[1].can_pop
        self.page.views.pop()
        top_view: ft.View = self.page.views[-1]
        self.page.route = top_view.route

    def goto(self, page: str = '/') -> None:
        self.page.go(page)