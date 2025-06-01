from exceptiongroup import catch
import flet as ft
import requests
from view.routes import RouteHandler
from utilities.file import File
from utilities.token import Token
from services import *
from view.modals.validation import ValidationModal
from myapp import MyApp

class MainWindow:
    def __init__(self, page: ft.Page, route_handler: RouteHandler, botconfig: dict, credentials: dict, bot_service: BotService, session_service: SessionService, websocket_service: WebsocketService):
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

        self.botconfig = botconfig
        self.credentials = credentials
        self.bot_services = bot_service
        self.websocket_service = websocket_service
        self.session_service = session_service
        self.load()
    
    def load(self) -> None:
        bot_credentials = self.credentials.get("bot")
        user_credentials = self.credentials.get("user")

        self.session_service.validation(user_credentials, self.botconfig, 'USER')
        self.page.go('/home')

        import asyncio
        asyncio.run(self.websocket_service.connect(self.session_service.user_account.credentials['access_token'], self.botconfig['client_id'], self.session_service.user_account.id))

        if self.session_service.validation(bot_credentials, self.botconfig, 'BOT'):
            self.bot_services.start(bot_credentials, self.botconfig,)
            File.save(MyApp.credentials_path, self.session_service.serialize())
        else:
            self.page.open(ValidationModal(bot_credentials, self.botconfig, self.bot_services, self.session_service))
