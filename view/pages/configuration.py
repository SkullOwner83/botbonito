import flet as ft
from models.appconfig import AppConfig
from ..controls import *
from services import *
from myapp import MyApp

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

    def restore_defaults(self) -> None:
        self.app_config.restore_defaults()

    def save_changes(self) -> None:
        self.app_config.language = self.language_dropdown.value
        self.app_config.theme = self.theme_dropdown.value
        self.app_config.client_id = self.client_id_textbox.value
        self.app_config.client_secret = self.client_secret_textbox.value
        
        self.app_config.social_media = {
            'facebook': self.facebook_textbox.value,
            'twitter': self.twitter_textbox.value,
            'instagram': self.instagram_textbox.value,
            'tiktok': self.tiktok_textbox.value,
            'youtube': self.youtube_textbox.value,
            'discord': self.discord_textbox.value
        }

        self.app_config.save(MyApp.botconfig_path)

    def set_controls(self) -> None:
        social_media = self.app_config.social_media
        self.client_id_textbox = TextBox(value=self.app_config.client_id, password=True, can_reveal_password=True)
        self.client_secret_textbox = TextBox(value=self.app_config.client_secret, password=True, can_reveal_password=True)
        self.redirect_uri_textbox = TextBox(value=self.app_config.redirect_uri, place_holder='https://localhost:300')
        self.facebook_textbox = TextBox(value=social_media.get('facebook'), height=32, border=0, expand=True, place_holder='https://facebook.com/username...')
        self.twitter_textbox = TextBox(value=social_media.get('twitter'), height=32, border=0, expand=True, place_holder='https://twitter.com/username...')
        self.instagram_textbox = TextBox(value=social_media.get('instagram'), height=32, border=0, expand=True, place_holder='https://instagram.com/username...')
        self.youtube_textbox = TextBox(value=social_media.get('youtube'), height=32, border=0, expand=True, place_holder='https://youtube.com/username...')
        self.discord_textbox = TextBox(value=social_media.get('discord'), height=32, border=0, expand=True, place_holder='https://discord.com/invite/...')
        self.tiktok_textbox = TextBox(value=social_media.get('tiktok'), height=32, border=0, expand=True, place_holder='https://tiktok.com/username...')

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
                                padding=0,
                                content=TabControl(
                                    tabs=[
                                        ft.Tab(
                                            text="General",
                                            content=ft.Container(
                                                padding=32,
                                                content=ft.Column(
                                                    scroll=ft.ScrollMode.ADAPTIVE,
                                                    spacing=20,
                                                    controls=[
                                                        ft.Column(
                                                            spacing=0,
                                                            controls=[
                                                                Label('Tema:'),
                                                                self.theme_dropdown
                                                            ]
                                                        ),

                                                        ft.Column(
                                                            spacing=0,
                                                            controls=[
                                                                Label('Lenguaje:'),
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
                                                                                ft.Image(width=32, src='social media/facebook.png'),
                                                                                self.facebook_textbox
                                                                            ]
                                                                        ),

                                                                        ft.Row(
                                                                            controls=[
                                                                                ft.Image(width=32, src='social media/instagram.png'),
                                                                                self.instagram_textbox
                                                                            ]
                                                                        ),

                                                                        ft.Row(
                                                                            controls=[
                                                                                ft.Image(width=32, src='social media/youtube.png'),
                                                                                self.youtube_textbox
                                                                            ]
                                                                        )
                                                                    ]
                                                                ),

                                                                ft.Column(
                                                                    expand=1,
                                                                    controls=[
                                                                        ft.Row(
                                                                            controls=[
                                                                                ft.Image(width=32, src='social media/twitter.png'),
                                                                                self.twitter_textbox
                                                                            ]
                                                                        ),

                                                                        ft.Row(
                                                                            controls=[
                                                                                ft.Image(width=32, src='social media/tiktok.png'),
                                                                                self.tiktok_textbox
                                                                            ]
                                                                        ),

                                                                        ft.Row(
                                                                            controls=[
                                                                                ft.Image(width=32, src='social media/discord.png'),
                                                                                self.discord_textbox
                                                                            ]
                                                                        ),
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ]
                                                )
                                            )
                                        ),

                                        ft.Tab(
                                            text='Seguridad',
                                            content=ft.Container(
                                                padding=32,
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
                                        )
                                    ]
                                )
                            ),

                            ft.Container(
                                padding=ft.padding.only(left=32, right=32, top=0, bottom=32),
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.END,
                                    controls=[
                                        Button(text='Restaurar', outlined=True, on_click=lambda e: self.restore_defaults()),
                                        Button(text='Guardar', outlined=False, on_click=lambda e: self.save_changes())
                                    ]
                                )
                            )
                        ]
                    )
                ]
            )
        )