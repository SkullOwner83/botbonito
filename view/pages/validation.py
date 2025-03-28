import webbrowser
import pyperclip
from modules.file import File
from modules.token import Token
from myapp import MyApp
import flet as ft

class ValidationPage:
    def __init__(self, page: ft.Page):
        self.page = page
        self.credentials = File.open(MyApp.credentials_path)
        self.botconfig = File.open(MyApp.botconfig_path)
        self.token = self.credentials['token']
        self.client_id = self.credentials['client_id']
        self.client_secret = self.credentials['client_secret']
        self.redirect_uri = self.botconfig['redirect_uri']
        self.scope = self.botconfig['scope']

    def get_view(self) -> ft.View:
        return ft.View(
            route = '/validation',
            padding=0,
            controls=[
                ft.Container(
                    expand=True,
                    content=ft.Column(
                        alignment= ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(value="Tu token no es válido.", size=32, weight=ft.FontWeight.BOLD),
                            ft.Text(value="Ingresa al siguiente sitio para obtener un nuevo token."),
                            ft.Container(
                                margin=ft.margin.only(top=32),
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls = [
                                        ft.Button(text="Abrir", width=100, on_click=lambda e: self.token_validation("OPEN")),
                                        ft.Button(text="Copiar", width=100, on_click=lambda e: self.token_validation("COPY"))
                                    ],
                                )
                            )
                        ]
                    )
                )
            ]
        )

    def token_validation(self, mode: str) -> None:
        token = Token(self.client_id, self.client_secret, self.scope, self.redirect_uri)
        auth_url = token.get_auth_link()

        if mode == 'OPEN':
            webbrowser.open(auth_url)

        if mode == 'COPY':
            pyperclip.copy(auth_url)

        NewToken = token.get_authorization()

        if token.validation(NewToken):
            self.credentials['token'] = NewToken
            File.save(MyApp.credentials_path, self.credentials)
            self.page.go('/')
            #self.run_bot()

        else:
            print("Token invalido")