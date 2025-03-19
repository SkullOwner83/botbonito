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
    
    def get_view(self) -> ft.Page:
        return ft.View(
            route = '/',
            controls=[
                ft.Row(controls=[ft.Text(value="Tu token no es valido. Ingresa al siguiente sitio para obtener un nuevo token.", )]),
                ft.Row(
                    controls = [
                        ft.Button(text="Abrir", width=100, on_click=self.token_validation),
                        ft.Button(text="Copiar", width=100)
                    ],
                    alignment = ft.MainAxisAlignment.CENTER 
                )
            ]
        )

    def token_validation(self, e: ft.ControlEvent):
        token = Token(self.client_id, self.client_secret, self.scope, self.redirect_uri)
        NewToken = token.get_authorization('copy_link')

        if token.validation(NewToken):
            self.credentials['token'] = NewToken
            File.save(MyApp.credentials_path, self.credentials)
            self.page.go('/')
            #self.run_bot()

        else:
            print("Token invalido")