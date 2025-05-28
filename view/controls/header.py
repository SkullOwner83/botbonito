from pydoc import text
import flet as ft
from services.session_service import SessionService
from utilities.file import File
from myapp import MyApp

class Header(ft.Container):
    def __init__(self, tile: str, botconfig: dict, session_service: SessionService):
        super().__init__()
        self.title = tile
        self.height = 64
        self.padding = ft.padding.symmetric(horizontal=32, vertical=12)
        self.border = ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_400))
        self.botconfig = botconfig
        self.session_service = session_service
        self.user = session_service.user_account
        
        self.set_controls()
        self.content = self.build()
        self.update_controls()

    def login(self) -> None:
        if self.session_service.login(self.botconfig, 'USER'):
            self.user = self.session_service.user_account
            self.update_controls()
            self.update()
            File.save(MyApp.credentials_path, self.session_service.serialize())

    def logout(self) -> None:
        self.session_service.logout('USER')
        self.update_controls()
        self.update()
        File.save(MyApp.credentials_path, self.session_service.serialize())

    def set_controls(self):
        self.profile_image = ft.Image(fit=ft.ImageFit.COVER)

        self.menu_button = ft.PopupMenuButton(
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
        )
    
    def update_controls(self):
        self.profile_image.src = self.user.profile_image if self.user else None
        self.profile_image.visible = self.session_service.is_logged_in

        self.menu_button.items = [
            ft.PopupMenuItem(text=self.user.username),
            ft.PopupMenuItem(text="Cerrar sesión", on_click=lambda e: self.logout())
        ] if self.session_service.is_logged_in else [
            ft.PopupMenuItem(text="Iniciar sesión", on_click=lambda e: self.login())
        ]

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

                            self.menu_button
                        ]
                    )
                )
            ]
        )
