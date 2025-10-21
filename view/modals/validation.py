import webbrowser
import pyperclip
import flet as ft
from models.appconfig import AppConfig
from myapp import MyApp
from utilities import *
from services import *
from ..controls import *

class ValidationModal(Modal):
    def __init__(self, credentials: dict, app_config: AppConfig) -> None:
        self.bot_service: BotService = ServiceLocator.get('bot')
        self.session_service: SessionService = ServiceLocator.get('session')
        self.websocket_service: WebsocketService = ServiceLocator.get('websocket')
        self.credentials = credentials
        self.app_config = app_config

        super().__init__(
            title="¡Token inválido!",
            actions_alignment=ft.MainAxisAlignment.CENTER,
            content=self.build(),
            actions=[
                Button(text="Abrir", width=100, on_click=lambda e: self.token_validation('OPEN')),
                Button(text="Copiar", width=100, on_click=lambda e: self.token_validation('COPY'))
            ]
        )

    def token_validation(self, mode: str):
        token = Token(self.app_config.client_id, self.app_config.client_secret, Constants.BOT_SCOPES, self.app_config.redirect_uri)
        auth_url = token.generate_auth_url()

        if mode == 'OPEN': webbrowser.open(auth_url)
        if mode == 'COPY': pyperclip.copy(auth_url)
        token_data = token.get_authorization()
        new_token = token_data.get('access_token')
        new_refresh_token = token_data.get('refresh_token')

        if token.validation(new_token):
            self.credentials.get('bot')['access_token'] = new_token
            self.credentials.get('bot')['refresh_token'] = new_refresh_token
            self.bot_service.bot_credentials = self.credentials
            self.session_service.load_account(self.credentials.get('bot'), self.app_config, AccountType.BOT)
            File.save(MyApp.credentials_path, self.session_service.serialize())
            self.bot_service.start()
            self.page.close(self)
            self.page.go('/')
        else:
            print("Token invalido")

    def build(self) -> ft.Column:
        return ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Text(value="Tu token no es válido. Ingresa al siguiente sitio para obtener un nuevo token.", font_family=MyApp.font_secondary, size=16),
            ]
        )