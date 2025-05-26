import flet as ft
import webbrowser
from services.session_service import SessionService
from modules.file import File
from modules.token import Token
from modules.api import Api
from myapp import MyApp

from models.user import User

class Header(ft.Container):
    def __init__(self, tile: str, botconfig: dict, session_service: SessionService):
        super().__init__()
        self.title = tile
        self.height = 64
        self.padding = ft.padding.symmetric(horizontal=32, vertical=12)
        self.border = ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_400))

        self.session_service = session_service
        self.user = session_service.user_account
        self.profile_image = ft.Image(src=self.user.profile_image if self.user else None, fit=ft.ImageFit.COVER, visible=session_service.is_logged_in)
        self.content = self.build()

        self.botconfig = botconfig

    def login(self) -> None:
        if self.session_service.login(self.botconfig):
            self.user = self.session_service.user_account
            self.profile_image.src = self.user.profile_image
            self.profile_image.visible = True
            self.profile_image.update()

    def logout(self) -> None:
        self.session_service.logout()
        self.profile_image.visible = False
        self.profile_image.update()

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
                                bgcolor=ft.Colors.WHITE,
                                menu_position=ft.PopupMenuPosition.UNDER,
                                elevation=8,
                                content=ft.Container(
                                    shape=ft.BoxShape.CIRCLE,
                                    bgcolor=ft.Colors.GREY_300,
                                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                    content=ft.Stack(
                                        alignment=ft.alignment.center,
                                        controls=[
                                            ft.Icon(name=ft.Icons.PERSON, color=ft.Colors.WHITE),
                                            self.profile_image
                                        ]
                                    )
                                ),
                                
                                items=[
                                    ft.PopupMenuItem(text="Iniciar sesión", on_click=lambda e: self.login()),
                                    ft.PopupMenuItem(text="Cerrar sesión", on_click=lambda e: self.logout())
                                ]
                            )
                        ]
                    )
                )
            ]
        )
