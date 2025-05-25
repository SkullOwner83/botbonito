import flet as ft
import webbrowser
from modules.file import File
from modules.token import Token
from modules.api import Api
from myapp import MyApp

from models.user import User

class Header(ft.Container):
    def __init__(self, tile):
        super().__init__()
        self.title = tile
        self.height = 64
        self.padding = ft.padding.symmetric(horizontal=32, vertical=12)
        self.border = ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_400))
        self.profile_image = ft.Image(fit=ft.ImageFit.COVER)
        self.session = False
        self.content = self.build()

        self.credentials = File.open(MyApp.credentials_path)
        self.botconfig = File.open(MyApp.botconfig_path)

    def login(self) -> None:
        token = Token(self.credentials['client_id'], self.credentials['client_secret'], ['user:read:email'], self.botconfig['redirect_uri'])
        auth_url = token.generate_auth_url()

        webbrowser.open(auth_url)
        token_data = token.get_authorization()
        api = Api(token_data['access_token'], self.credentials['client_id'])
        user_data= api.get_user()
        self.profile_image.src = user_data['profile_image_url']
        self.profile_image.update()
        self.session = True

    def build(self) -> ft.Row:
        return ft.Row(
            spacing=0,
            controls= [
                ft.Container(
                    ft.Text(
                        value=self.title,
                        font_family=MyApp.font_primary,
                        weight=ft.FontWeight.BOLD,
                        size=24
                    )
                ),

                ft.Container(
                    expand=True,
                    alignment=ft.alignment.center_right,
                    content=ft.Row(
                        alignment= ft.MainAxisAlignment.END,
                        controls=[
                            ft.IconButton(
                                width=40,
                                height=40,
                                icon=ft.Icons.NOTIFICATIONS,
                            ),

                            ft.PopupMenuButton(
                                width=40,
                                height=40,
                                tooltip=None,
                                menu_position=ft.PopupMenuPosition.UNDER,
                                elevation=8,
                                content=ft.Container(
                                    shape=ft.BoxShape.CIRCLE,
                                    bgcolor=ft.Colors.GREY_300,
                                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                    content=self.profile_image
                                ),
                                items=[
                                    ft.PopupMenuItem(text="Iniciar sesión", on_click=lambda e: self.login())
                                ]
                            )
                        ]
                    )
                )
            ]
        )
