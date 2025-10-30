import flet as ft
from models.appconfig import AppConfig
from ..controls import *
from services import *


class HomePage(ft.Container):
    def __init__(self, page: ft.Page, app_config: AppConfig) -> None:
        self.page = page
        self.app_config = app_config
        super().__init__(padding=32, content=self.build())

    def build(self) -> ft.Container:
        return ft.Column(
            spacing=20,
            controls=[
                ft.Row(
                    height=32,
                    controls=[
                        ft.IconButton(width=32, icon=ft.Icons.ARROW_BACK_IOS_ROUNDED),

                        ft.Container(
                            expand=True,
                            bgcolor=ft.Colors.WHITE,
                            alignment=ft.alignment.center,
                            border_radius=8,
                            content=ft.Text(
                                value="jueves, 22 de mayo",
                                color=ft.Colors.PRIMARY,
                                weight=ft.FontWeight.BOLD,
                                size=16
                            )
                        ),

                        ft.IconButton(width=32, icon=ft.Icons.ARROW_FORWARD_IOS_ROUNDED)
                    ]
                ),

                ft.ResponsiveRow(
                    columns=4,
                    spacing=20,
                    run_spacing=20,
                    controls=[
                        Card(title='seguidores', value='0', icon=ft.Icons.FAVORITE, col={ "xs": 4, "sm": 2, "md": 1 }),
                        Card(title='suscriptores', value='0', icon=ft.Icons.STAR, col={ "xs": 4, "sm": 2, "md": 1 }),
                        Card(title='vistas', value='0', icon=ft.Icons.REMOVE_RED_EYE, col={ "xs": 4, "sm": 2, "md": 1 }),
                        Card(title='bits', value='0', icon=ft.Icons.PAYMENTS, col={ "xs": 4, "sm": 2, "md": 1 })
                    ]
                )
            ]
        )