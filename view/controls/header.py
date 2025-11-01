import webbrowser
import flet as ft
from models.appconfig import AppConfig
from utilities.enums import AccountType
from services import *
from utilities.file import File
from myapp import MyApp

class Header(ft.Container):
    def __init__(self, title: str, app_config: AppConfig) -> None:
        super().__init__()
        self.title = title
        self.height = 64
        self.padding = ft.padding.symmetric(horizontal=32)
        self.border = ft.border.only(bottom=ft.border.BorderSide(1, ft.Colors.GREY_400))
        self.app_config = app_config

        self.session_service: SessionService = ServiceLocator.get('session')
        self.websocket_service: WebsocketService = ServiceLocator.get('websocket')
        self.bot_service: BotService = ServiceLocator.get('bot')
        self.user = self.session_service.user_account

        self.session_service.on_validate_callback.append(self.on_validate)
        self.websocket_service.stream_online_callback.append(self.on_stream_online)
        self.websocket_service.stream_offline_callback.append(self.on_stream_offline)
        
        self.set_controls()
        self.content = self.build()
        self.update_controls()

    def login(self) -> None:
        if self.session_service.login(self.app_config, AccountType.USER):
            self.user = self.session_service.user_account
            
            if not self.user.username in self.app_config.channels:
                self.app_config.channels.append(self.user.username)

            self.app_config.save(MyApp.appconfig_path)
            File.save(MyApp.credentials_path, self.session_service.serialize())
            self.update_controls()
            self.update()

            if not self.bot_service.is_running:
                self.bot_service.start()

    def logout(self) -> None:
        self.session_service.logout(AccountType.USER)
        self.user = None
        self.app_config.channels.clear()
        self.app_config.save(MyApp.appconfig_path)
        File.save(MyApp.credentials_path, self.session_service.serialize())
        self.update_controls()
        self.update()

        if self.bot_service.is_running:
            self.bot_service.stop()

    def on_validate(self) -> None:
        self.user = self.session_service.user_account
        self.update_controls()
        self.update()

    def on_stream_online(self, payload) -> None:
        self.stream_status_text.value = 'Online'
        self.status_dot.bgcolor = ft.Colors.GREEN
        if self.page: self.update()

    def on_stream_offline(self, payload) -> None:
        self.stream_status_text.value = 'Offline'
        self.status_dot.bgcolor = ft.Colors.RED
        if self.page: self.update()

    def set_controls(self) -> None:
        self.profile_image = ft.Image(fit=ft.ImageFit.COVER)
        self.username_text = ft.Text(value='Usuario', font_family=MyApp.font_primary, size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY, selectable=True)
        self.stream_status_text = ft.Text(value='Offline', font_family=MyApp.font_secondary, size=16, weight=ft.FontWeight.BOLD)
        self.status_dot = ft.Container(width=12, shape=ft.BoxShape.CIRCLE, bgcolor=ft.Colors.RED, content=ft.Text(''))

        self.title_text = ft.Text(
            value=self.title,
            font_family=MyApp.font_primary,
            weight=ft.FontWeight.BOLD,
            size=24
        )

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
    
    def update_controls(self) -> None:
        self.profile_image.src = self.user.profile_image if self.user else None
        self.profile_image.visible = self.session_service.is_logged_in
        self.username_text.value = self.user.display_name if self.user else None
        self.user_status.visible = True if self.session_service.is_logged_in else False

        self.menu_button.items = [
            ft.PopupMenuItem(text='Mi canal', height=32, icon=ft.Icons.PERSON_ROUNDED, on_click=lambda e: webbrowser.open(f'https://www.twitch.tv/{self.session_service.user_account.username}')),
            ft.PopupMenuItem(text='Configuración', height=32, icon=ft.Icons.SETTINGS_ROUNDED, on_click=lambda e: self.page.go('/configuration')),
            ft.PopupMenuItem(text='Cerrar sesión', height=32, icon=ft.Icons.LOGOUT_ROUNDED, on_click=lambda e: self.logout())
        ] if self.session_service.is_logged_in else [
            ft.PopupMenuItem(text='Iniciar sesión', height=32, icon=ft.Icons.LOGIN_ROUNDED, on_click=lambda e: self.login())
        ]

    def set_title(self, new_title):
        self.title_text.value = new_title
        self.title_text.update()

    def build(self) -> ft.Row:
        return ft.Row(
            spacing=0,
            controls= [
                ft.Container(
                    expand=True,
                    content=self.title_text
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
