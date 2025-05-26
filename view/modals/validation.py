import webbrowser
import pyperclip
import flet as ft
from myapp import MyApp
from modules.token import Token
from modules.file import File
from services.botservice import BotService
from ..controls import *

class ValidationModal(Modal):
    def __init__(self, credentials: dict, botconfig: dict, bot_service: BotService) -> None:
        self.bot_service = bot_service
        self.credentials = credentials
        self.botconfig = botconfig

        super().__init__(
            title="¡Token inválido!",
            actions_alignment=ft.MainAxisAlignment.CENTER,
            content=self.build(),
            actions=[
                Button(text="Abrir", width=100, on_click=lambda e: self.token_validation("OPEN")),
                Button(text="Copiar", width=100, on_click=lambda e: self.token_validation("COPY"))
            ]
        )

    def token_validation(self, mode: str):
        token = Token(self.botconfig['client_id'], self.botconfig['client_secret'], self.botconfig['scope'], self.botconfig['redirect_uri'])
        auth_url = token.generate_auth_url()

        if mode == 'OPEN': webbrowser.open(auth_url)
        if mode == 'COPY': pyperclip.copy(auth_url)
        token_data = token.get_authorization()
        new_token = token_data.get('access_token')
        new_refresh_token = token_data.get('refresh_token')

        if token.validation(new_token):
            self.credentials['access_token'] = new_token
            self.credentials['refresh_token'] = new_refresh_token
            #File.save(MyApp.credentials_path, self.credentials)
            self.bot_service.start(self.credentials, self.botconfig)
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