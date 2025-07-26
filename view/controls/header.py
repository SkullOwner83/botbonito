import webbrowser
import flet as ft
from utilities.enums import AccountType
from services import *
from utilities.file import File
from myapp import MyApp

class Header(ft.Container):
    def __init__(self, tile: str, botconfig: dict) -> None:
        super().__init__()
        self.title = tile
        self.height = 64
        self.padding = ft.padding.symmetric(horizontal=32)
        self.border = ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_400))
        self.botconfig = botconfig

        self.session_service: SessionService = ServiceLocator.get('session')
        self.websocket_service: WebsocketService = ServiceLocator.get('websocket')
        self.user = self.session_service.user_account

        self.websocket_service.stream_online_callback.append(self.on_stream_online)
        self.websocket_service.stream_offline_callback.append(self.on_stream_offline)
        
        self.set_controls()
        self.content = self.build()
        self.update_controls()

    def on_stream_online(self, payload):
        self.stream_status_text.value = 'Online'
        self.status_dot.bgcolor = ft.Colors.GREEN
        if self.page: self.update()

    def on_stream_offline(self, payload):
        self.stream_status_text.value = 'Offline'
        self.status_dot.bgcolor = ft.Colors.RED
        if self.page: self.update()

    def login(self) -> None:
        if self.session_service.login(self.botconfig, AccountType.USER):
            self.user = self.session_service.user_account
            self.update_controls()
            self.update()
            File.save(MyApp.credentials_path, self.session_service.serialize())

    def logout(self) -> None:
        self.session_service.logout(AccountType.USER)
        self.update_controls()
        self.update()
        File.save(MyApp.credentials_path, self.session_service.serialize())

    def set_controls(self):
        self.profile_image = ft.Image(fit=ft.ImageFit.COVER)
        self.username_text = ft.Text(value='Usuario', font_family=MyApp.font_primary, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY, selectable=True)
        self.stream_status_text = ft.Text(value='Offline', font_family=MyApp.font_secondary, size=16, weight=ft.FontWeight.BOLD)
        self.status_dot = ft.Container(width=12, shape=ft.BoxShape.CIRCLE, bgcolor=ft.Colors.RED, content=ft.Text(''))

        self.user_status = ft.Column(
            spacing=-4,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                self.username_text,
                ft.Row(
                    spacing=4,
                    controls=[
                        self.status_dot,
                        self.stream_status_text
                    ]
                )
            ]
        )

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
        self.username_text.value = self.user.display_name if self.user else None
        self.user_status.visible = True if self.session_service.is_logged_in else False

        self.menu_button.items = [
            ft.PopupMenuItem(text='Mi canal', on_click=lambda e: webbrowser.open(f'https://www.twitch.tv/{self.session_service.user_account.username}')),
            ft.PopupMenuItem(text='Configuración', on_click=lambda e: self.page.go('/configuration')),
            ft.PopupMenuItem(text='Cerrar sesión', on_click=lambda e: self.logout())
        ] if self.session_service.is_logged_in else [
            ft.PopupMenuItem(text='Iniciar sesión', on_click=lambda e: self.login())
        ]

    def build(self) -> ft.Row:
        return ft.Row(
            spacing=0,
            controls= [
                ft.Container(
                    expand=True,
                    content=ft.Text(
                        value=self.title,
                        font_family=MyApp.font_primary,
                        weight=ft.FontWeight.BOLD,
                        size=24
                    )
                ),

                ft.Container(
                    alignment=ft.alignment.center_right,
                    content=ft.Row(
                        alignment= ft.MainAxisAlignment.END,
                        controls=[
                            self.user_status,
                            self.menu_button,
                        ]
                    )
                )
            ]
        )
