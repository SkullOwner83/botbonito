import webbrowser
import pyperclip
from typing import Callable, Optional
from services.botservices import BotServices
import flet as ft
from modules.token import Token
from modules.file import File
from myapp import MyApp
from ..controls import *

class ValidationModal(Modal):
    def __init__(self, bot_service: BotServices) -> None:
        self.credentials = File.open(MyApp.credentials_path)
        self.botconfig = File.open(MyApp.botconfig_path)
        self.token = self.credentials['token']
        self.client_id = self.credentials['client_id']
        self.client_secret = self.credentials['client_secret']
        self.redirect_uri = self.botconfig['redirect_uri']
        self.scope = self.botconfig['scope']
        self.bot_service = bot_service

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
        token = Token(self.client_id, self.client_secret, self.scope, self.redirect_uri)
        auth_url = token.generate_auth_url()

        if mode == 'OPEN': webbrowser.open(auth_url)
        if mode == 'COPY': pyperclip.copy(auth_url)
        token_data = token.get_authorization()
        new_token = token_data.get('access_token')
        new_refresh_token = token_data.get('refresh_token')

        if token.validation(new_token):
            self.credentials['token'] = new_token
            self.credentials['refresh_token'] = new_refresh_token
            File.save(MyApp.credentials_path, self.credentials)
            self.bot_service.start(self.botconfig, self.credentials)
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