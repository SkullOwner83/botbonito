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
            case "/home": self.layout.set_view(HomePage(self.page, self.app_config), 'Dashboard')
            case "/commands": self.layout.set_view(CommandsPage(self.page, self.app_config), 'Comandos')
            case "/events": self.layout.set_view(EventsPage(self.page, self.app_config), 'Eventos')
            case "/moderation": self.layout.set_view(ModerationPage(self.page, self.app_config), 'Moderación')
            case "/configuration": self.layout.set_view(ConfigurationPage(self.page, self.app_config), 'Configuración')
            case _: self.layout.set_view(HomePage(self.page, self.app_config), 'Dashboard')

    def goto(self, page: str = '/') -> None:
        self.page.go(page)