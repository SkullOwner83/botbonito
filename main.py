import sys
sys.path.append(r'D:\Desktop\Proyectos\Visual Studio Code\botbonito')
from flet import Page, Theme, app
from flet import PageTransitionsTheme, PageTransitionTheme
from view.routes import RouteHandler
from modules.token import Token
from myapp import MyApp
from modules.file import File
from services.botservices import BotServices
from view.modals import *

class BotUI:
    def __init__(self, page: Page):
        self.page = page
        self.title = "Botbonito"
        self.page.title = self.title
        self.page.window.width = 800
        self.page.window.height = 600
        self.page.window.always_on_top = False

        page.theme = Theme(
            page_transitions=PageTransitionsTheme(
                windows=PageTransitionTheme.NONE
            )
        )

        self.start_up()
    
    def start_up(self) -> None:
        self.bot_services = BotServices()
        self.route_handler = RouteHandler(self.page, self.bot_services)
        self.page.on_route_change = self.route_handler.route_change
        #self.page.on_view_pop = self.route_handler.view_pop
        self.page.go(self.page.route)
        self.page.update()

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

if __name__ == "__main__":
    app(
        target=lambda page: BotUI(page),
        assets_dir='assets'
        #view=ft.WEB_BROWSER,
    )