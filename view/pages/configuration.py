import flet as ft
from models.appconfig import AppConfig
from ..controls import *
from services import *

class ConfigurationPage(ft.View):
    def __init__(self, page: ft.Page, app_config: AppConfig) -> None:
        super().__init__(
            route='/configuration',
            padding=0,
        )

        self.page = page
        self.app_config = app_config
        self.set_controls()
        self.controls.append(self.build())

    def set_controls(self) -> None:
        social_media = self.app_config.social_media
        self.redirect_uri_textbox = TextBox(value=self.app_config.redirect_uri, place_holder='https://localhost:300')
        self.client_id_textbox = TextBox(value=self.app_config.client_id)
        self.client_secret_textbox = TextBox(value=self.app_config.client_id)
        self.facebook_textbox = TextBox(value=social_media['facebook'], height=32, border=0, expand=True, place_holder='https://facebook.com/username')
        self.twitter_textbox = TextBox(value=social_media['twitter'], height=32, border=0, expand=True, place_holder='https://twitter.com/username')
        self.instagram_textbox = TextBox(value=social_media['instagram'], height=32, border=0, expand=True, place_holder='https://instagram.com/username')
        self.youtube_textbox = TextBox(value=social_media['youtube'], height=32, border=0, expand=True, place_holder='https://youtube.com/username')
        self.discord_textbox = TextBox(value=social_media['discord'], height=32, border=0, expand=True, place_holder='https://discord.com/username')
        self.tiktok_textbox = TextBox(value=social_media['tiktok'], height=32, border=0, expand=True, place_holder='https://tiktok.com/username')

        self.theme_dropdown = DropDown(
            value=self.app_config.theme,
            options=[
                ft.DropdownOption(key='light', text='Claro'),
                ft.DropdownOption(key='dark', text='Oscuro')
            ]
        )

        self.language_dropdown = DropDown(
            value=self.app_config.language,
            options=[
                ft.DropdownOption(key='español', text='Español'),
                ft.DropdownOption(key='english', text='English')
            ]
        )

    def build(self) -> ft.Container:
        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.GREY_100,
            content=ft.Row(
                expand=True,
                spacing=0,
                controls =[
                    NavigationBar(self.page),

                    ft.Column(
                        expand=True,
                        spacing=0,
                        controls=[
                            Header("Configuración", self.app_config),

                            ft.Container(
                                expand=True,
                                padding=32,
                                alignment=ft.alignment.center,
                                content=ft.Tabs(
                                    tabs=[
                                        ft.Tab(
                                            text="General",
                                            content=ft.Column(
                                                spacing=20,
                                                controls=[
                                                    ft.Column(
                                                        spacing=0,
                                                        controls=[
                                                            Label('Thema'),
                                                            self.theme_dropdown
                                                        ]
                                                    ),

                                                    ft.Column(
                                                        spacing=0,
                                                        controls=[
                                                            Label('Lenguaje'),
                                                            self.language_dropdown
                                                        ]
                                                    ),

                                                    Label('Redes sociales:'),
                                                    ft.Row(
                                                        spacing=20,
                                                        controls=[
                                                            ft.Column(
                                                                expand=1,
                                                                controls=[
                                                                    ft.Row(
                                                                        controls=[
                                                                            ft.Image(width=32, src='facebook.png'),
                                                                            self.facebook_textbox
                                                                        ]
                                                                    ),

                                                                    ft.Row(
                                                                        controls=[
                                                                            ft.Image(width=32, src='twitter.png'),
                                                                            self.twitter_textbox
                                                                        ]
                                                                    ),

                                                                    ft.Row(
                                                                        controls=[
                                                                            ft.Image(width=32, src='instagram.png'),
                                                                            self.instagram_textbox
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    )
                                                ]
                                            )
                                        ),

                                        ft.Tab(
                                            text='Seguridad',
                                            content=ft.Column(
                                                spacing=16,
                                                controls=[
                                                    ft.Column(
                                                        spacing=0,
                                                        controls=[
                                                            Label('Client ID:'),
                                                            self.client_id_textbox
                                                        ]
                                                    ),

                                                    ft.Column(
                                                        spacing=0,
                                                        controls=[
                                                            Label('Client secret:'),
                                                            self.client_secret_textbox
                                                        ]
                                                    ),

                                                    ft.Column(
                                                        spacing=0,
                                                        controls=[
                                                            Label('Dirección de redireccionamiento de OAuth:'),
                                                            self.redirect_uri_textbox
                                                        ]
                                                    ),
                                                ]
                                            )
                                        )
                                    ]
                                )
                            )
                        ]
                    )
                ]
            )
        )