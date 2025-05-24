import flet as ft
from view.routes import RouteHandler
from modules.file import File
from modules.token import Token
from services.botservice import BotService
from view.modals.validation import ValidationModal
from myapp import MyApp

class MainWindow:
    def __init__(self, page: ft.Page, route_handler: RouteHandler, bot_service: BotService):
        self.page = page
        self.title = "Botbonito"
        self.page.title = self.title
        self.page.window.width = 800
        self.page.window.height = 600
        self.page.window.always_on_top = False
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

        self.bot_services = bot_service
        self.load()
    
    def load(self) -> None:
        credentials = File.open(MyApp.credentials_path)
        botconfig = File.open(MyApp.botconfig_path)
        access_token = credentials.get('token')
        refresh_token = credentials.get('refresh_token')

        if Token.validation(access_token):
            self.bot_services.start(botconfig, credentials)
            self.page.go('/')
        else:
            if refresh_token:
                token = Token(credentials['client_id'], credentials['client_secret'], botconfig['scope'], botconfig['redirect_uri'])
                token_refreshed = token.refresh_access_token(credentials['refresh_token'])
                new_token = token_refreshed.get('access_token')
                new_refresh_token = token_refreshed.get('refresh_token')

                if Token.validation(new_token):
                    credentials['token'] = new_token
                    credentials['refresh_token'] = new_refresh_token
                    File.save(MyApp.credentials_path, credentials)
                    print("Token has been refreshed.")
                    self.bot_services.start(botconfig, credentials)
                    self.page.go('/')
                    return

            self.page.open(ValidationModal(self.bot_services))