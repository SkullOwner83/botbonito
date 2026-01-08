import asyncio
import flet as ft
from models.appconfig import AppConfig
from utilities.enums import AccountType
from view.routes import RouteHandler
from utilities.file import File
from services import *
from view.modals.validation import ValidationModal
from myapp import MyApp
from .theme import Theme

class MainWindow(ft.View):
    def __init__(self, page: ft.Page, route_handler: RouteHandler, app_config: AppConfig, credentials: dict) -> None:
        self.page = page
        self.title = "Botbonito"
        self.page.title = self.title
        self.page.window.width = 800
        self.page.window.height = 600
        self.page.window.always_on_top = True
        self.page.on_route_change = route_handler.route_change
        # self.page.window.title_bar_hidden = True

        self.app_config = app_config
        self.credentials = credentials
        self.route_handler = route_handler
        self.bot_service: BotService = ServiceLocator.get('bot')
        self.websocket_service: WebsocketService = ServiceLocator.get('websocket')
        self.session_service: SessionService = ServiceLocator.get('session')
        
        Theme.apply(self.page, app_config.theme)
        self.page.go(self.page.route)
        self.page.update()
        self.load()

    def load(self) -> None:
        bot_credentials = self.credentials.get('bot')
        user_credentials = self.credentials.get('user')

        if self.session_service.validation(user_credentials, self.app_config, AccountType.USER):
            self.page.go('/home')
            

        if self.session_service.validation(bot_credentials, self.app_config, AccountType.BOT):
            self.bot_service.bot_credentials = bot_credentials
            self.app_config.channels = ['skullowner_', 'el_colunga']
            self.bot_service.app_config = self.app_config


            self.bot_service.start()
            File.save(MyApp.credentials_path, self.session_service.serialize())
            
            if self.session_service.is_logged_in:
                asyncio.run(
                    self.websocket_service.connect(
                        self.session_service.user_account.credentials['access_token'], 
                        self.app_config.client_id, 
                        self.session_service.user_account.id
                    )
                )
        else:
            self.page.open(ValidationModal(self.credentials, self.app_config))

