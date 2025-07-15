import asyncio
import flet as ft
from models.appconfig import AppConfig
from utilities.enums import AccountType
from view.routes import RouteHandler
from utilities.file import File
from services import *
from view.modals.validation import ValidationModal
from myapp import MyApp

class MainWindow:
    def __init__(self, page: ft.Page, route_handler: RouteHandler, app_config: AppConfig, credentials: dict) -> None:
        self.page = page
        self.title = "Botbonito"
        self.page.title = self.title
        self.page.window.width = 800
        self.page.window.height = 600
        self.page.window.always_on_top = True
        self.page.on_route_change = route_handler.route_change
        #self.page.on_view_pop =route_handler.view_pop
        self.page.go(self.page.route)
        self.page.update()

        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=ft.Colors.DEEP_PURPLE,
                on_primary=ft.Colors.WHITE,
            ),
            page_transitions=ft.PageTransitionsTheme(
                windows=ft.PageTransitionTheme.NONE
            )
        )

        self.app_config = app_config
        self.credentials = credentials
        self.bot_services: BotService = ServiceLocator.get('bot')
        self.websocket_service: WebsocketService = ServiceLocator.get('websocket')
        self.session_service: SessionService = ServiceLocator.get('session')
        self.load()
    
    def load(self) -> None:
        bot_credentials = self.credentials.get("bot")
        user_credentials = self.credentials.get("user")
        self.session_service.validation(user_credentials, self.app_config, AccountType.USER)
        self.page.go('/home')

        if self.session_service.validation(bot_credentials, self.app_config, AccountType.BOT):
            self.bot_services.start(bot_credentials, self.app_config,)
            File.save(MyApp.credentials_path, self.session_service.serialize())
            
            if self.session_service.is_logged_in:
                asyncio.run(self.websocket_service.connect(self.session_service.user_account.credentials['access_token'], self.app_config.client_id, self.session_service.user_account.id))
        else:
            self.page.open(ValidationModal(bot_credentials, self.app_config))
